import { Pool } from 'pg';
import * as fs from 'fs';
import * as path from 'path';

const TEXTS_DIR = 'texts';
const CHUNK_SIZE = 500;

const THINKER_MAPPING: Record<string, string[]> = {
  'freud': ['freud/'],
  'kuczynski': [
    'A_Priori_Knowledge', 'Analytic_Philosophy', 'Attachment_Theory', 'Chomskys_Two',
    'Conception_and_Causation', 'Counterfactuals', 'Dialogue_Concerning', 'Dialogues_with_the_Master',
    'Group_Psychology', 'Incompleteness', 'Intensionality', 'Kant_and_Hume', 'King_Follett',
    'Libets_Experiment', 'Logic_Set_Theory', 'Mind_Meaning', 'Moral_Structure', 'Network_Reinterpretation',
    'Ninety_Paradoxes', 'OCD_and_Philosophy', 'Outline_of_a_Theory', 'Papers_on_Accounting',
    'Philosophical_Knowledge', 'Quantifiers', 'Theoretical_Knowledge', 'Three_Kinds_of_Psychopaths',
    'Why_Was_Socrates', 'Berkeley', 'AA_Secular', 'Russell_Theory', 'Personal_Objectual', 'Causality',
    'College_Papers', 'Dialogue_About', 'AI_and_Philosophy', 'Ask_Me_Anything', 'Actual_Intelligence',
    'Aesthetic_Relativism', 'Astrology_Psychoanalysis', 'Causal_Dependence', 'Autistic_People',
    'Determinism', 'Set_Theory', 'Observations', 'Originalism', 'Case_for_Financial', 'Descriptions_and_Beyond',
    'Ego_Syntonic', 'Functional_vs_Structural', 'Kant_in_2020', 'Literal_Meaning', 'Philosophical_Positions',
    'OCD_Short_Papers'
  ],
  'jung': ['jung/'],
  'hume': ['hume/'],
  'nietzsche': ['nietzsche/'],
  'bergler': ['bergler/']
};

function identifyThinker(filepath: string): string {
  for (const [thinker, patterns] of Object.entries(THINKER_MAPPING)) {
    for (const pattern of patterns) {
      if (filepath.includes(pattern)) {
        return thinker;
      }
    }
  }
  return 'kuczynski';
}

function chunkText(text: string, chunkSize: number = 500): string[] {
  const words = text.split(/\s+/);
  const chunks: string[] = [];
  let currentChunk: string[] = [];
  
  for (const word of words) {
    currentChunk.push(word);
    if (currentChunk.length >= chunkSize) {
      chunks.push(currentChunk.join(' '));
      currentChunk = [];
    }
  }
  
  if (currentChunk.length > 0) {
    chunks.push(currentChunk.join(' '));
  }
  
  return chunks;
}

function cleanText(text: string): string {
  return text
    .replace(/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/g, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function getAllTextFiles(dir: string): string[] {
  const files: string[] = [];
  
  function walkDir(currentDir: string) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);
      if (entry.isDirectory()) {
        walkDir(fullPath);
      } else if (entry.name.endsWith('.txt')) {
        files.push(fullPath);
      }
    }
  }
  
  walkDir(dir);
  return files;
}

async function main() {
  const databaseUrl = process.env.DATABASE_URL;
  if (!databaseUrl) {
    console.error('DATABASE_URL not set');
    process.exit(1);
  }

  const pool = new Pool({ connectionString: databaseUrl });
  
  console.log('Connecting to database...');
  const client = await pool.connect();
  
  try {
    console.log('Clearing existing chunks...');
    await client.query('TRUNCATE TABLE text_chunks RESTART IDENTITY');
    
    const allRecords: [string, string, string, number][] = [];
    let filesProcessed = 0;
    
    const textFiles = getAllTextFiles(TEXTS_DIR);
    console.log(`Found ${textFiles.length} text files`);
    
    for (const filepath of textFiles) {
      const relativePath = path.relative(TEXTS_DIR, filepath);
      const thinker = identifyThinker(relativePath);
      
      console.log(`Processing: ${relativePath} -> ${thinker}`);
      
      let content: string;
      try {
        content = fs.readFileSync(filepath, 'utf-8');
      } catch (e) {
        console.error(`  Error reading file: ${e}`);
        continue;
      }
      
      content = cleanText(content);
      if (content.length < 100) {
        console.log('  Skipping (too short)');
        continue;
      }
      
      const chunks = chunkText(content, CHUNK_SIZE);
      console.log(`  Created ${chunks.length} chunks`);
      
      for (let idx = 0; idx < chunks.length; idx++) {
        allRecords.push([thinker, relativePath, chunks[idx], idx]);
      }
      
      filesProcessed++;
    }
    
    console.log(`\nInserting ${allRecords.length} chunks into database...`);
    
    const batchSize = 500;
    for (let i = 0; i < allRecords.length; i += batchSize) {
      const batch = allRecords.slice(i, i + batchSize);
      const values: string[] = [];
      const params: any[] = [];
      
      batch.forEach((record, idx) => {
        const offset = idx * 4;
        values.push(`($${offset + 1}, $${offset + 2}, $${offset + 3}, $${offset + 4})`);
        params.push(...record);
      });
      
      await client.query(
        `INSERT INTO text_chunks (thinker, source_file, chunk_text, chunk_index) VALUES ${values.join(', ')}`,
        params
      );
    }
    
    console.log('Done!');
    
    const result = await client.query(
      'SELECT thinker, COUNT(*) as count FROM text_chunks GROUP BY thinker ORDER BY count DESC'
    );
    
    console.log('\n' + '='.repeat(50));
    console.log('CHUNKING COMPLETE');
    console.log('='.repeat(50));
    console.log(`Files processed: ${filesProcessed}`);
    console.log(`Total chunks inserted: ${allRecords.length}`);
    console.log('\nChunks by thinker:');
    for (const row of result.rows) {
      console.log(`  ${row.thinker}: ${row.count}`);
    }
    
  } finally {
    client.release();
    await pool.end();
  }
}

main().catch(console.error);
