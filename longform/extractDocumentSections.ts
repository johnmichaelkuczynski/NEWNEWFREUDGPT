export interface DocumentSection {
  title: string;
  text: string;
  level: number;
}

const HEADING_PATTERNS = [
  /^(Part\s+\d+[.:]\s*.*)$/im,
  /^(§+\s*.*)$/m,
  /^((?:I{1,3}|IV|V|VI{0,3}|IX|X)[.:]\s*.*)$/m,
  /^(\d+[.:]\s+[A-Z].*)$/m,
  /^(Chapter\s+\d+[.:]\s*.*)$/im,
  /^(Section\s+\d+[.:]\s*.*)$/im,
  /^([A-Z][A-Z\s]{5,}[A-Z])$/m,
];

export function extractDocumentSections(fullText: string): DocumentSection[] {
  const lines = fullText.split("\n");
  const sections: DocumentSection[] = [];
  
  let currentTitle = "Introduction";
  let currentText: string[] = [];
  let currentLevel = 0;
  
  for (const line of lines) {
    let isHeading = false;
    let headingTitle = "";
    let headingLevel = 1;
    
    for (let i = 0; i < HEADING_PATTERNS.length; i++) {
      const match = line.trim().match(HEADING_PATTERNS[i]);
      if (match && match[1]) {
        isHeading = true;
        headingTitle = match[1].trim();
        headingLevel = i < 2 ? 1 : 2;
        break;
      }
    }
    
    if (isHeading) {
      if (currentText.length > 0) {
        const text = currentText.join("\n").trim();
        if (text.length > 50) {
          sections.push({
            title: currentTitle,
            text: text,
            level: currentLevel,
          });
        }
      }
      currentTitle = headingTitle;
      currentLevel = headingLevel;
      currentText = [];
    } else {
      currentText.push(line);
    }
  }
  
  if (currentText.length > 0) {
    const text = currentText.join("\n").trim();
    if (text.length > 50) {
      sections.push({
        title: currentTitle,
        text: text,
        level: currentLevel,
      });
    }
  }
  
  if (sections.length === 0) {
    const chunks = chunkByParagraphs(fullText, 2000);
    return chunks.map((chunk, i) => ({
      title: `Section ${i + 1}`,
      text: chunk,
      level: 1,
    }));
  }
  
  return sections;
}

function chunkByParagraphs(text: string, maxChars: number): string[] {
  const paragraphs = text.split(/\n\s*\n/);
  const chunks: string[] = [];
  let current = "";
  
  for (const para of paragraphs) {
    if (current.length + para.length > maxChars && current.length > 0) {
      chunks.push(current.trim());
      current = para;
    } else {
      current += (current ? "\n\n" : "") + para;
    }
  }
  
  if (current.trim()) {
    chunks.push(current.trim());
  }
  
  return chunks;
}
