class ThinkerWorkshop {
    constructor() {
        this.dialoguePanel = document.getElementById('dialogue-panel');
        this.archivePanel = document.getElementById('archive-panel');
        this.messageContainer = document.getElementById('messages');
        this.sourcesDisplay = document.getElementById('sources-display');
        this.userInput = document.getElementById('user-input');
        this.sendButton = document.getElementById('submit-btn');
        this.uploadButton = document.getElementById('upload-btn');
        this.fileInput = document.getElementById('file-input');
        this.userStatus = document.getElementById('user-status');
        this.providerSelect = document.getElementById('provider-select');
        this.modelSelect = document.getElementById('model-select');
        this.creativitySlider = document.getElementById('creativity-level');
        this.creativityValue = document.getElementById('creativity-level-value');
        this.answerLengthSlider = document.getElementById('answer-length');
        this.answerLengthValue = document.getElementById('answer-length-value');
        this.quoteCountSlider = document.getElementById('quote-count');
        this.quoteCountValue = document.getElementById('quote-count-value');
        this.fontSizeSlider = document.getElementById('font-size-slider');
        this.fontSizeValue = document.getElementById('font-size-value');
        this.responseModeSelect = document.getElementById('response-mode-select');
        this.dataSourceSelect = document.getElementById('data-source-select');
        this.knowledgePanel = document.getElementById('knowledge-panel');
        this.avatarButtons = document.querySelectorAll('.avatar-btn');
        
        this.databases = [];
        this.providers = [];
        this.selectedDatabase = 'freud';
        this.currentEventSource = null;
        this.currentSources = [];
        this.knowledgeQuotes = [];
        this.knowledgeFacts = [];
        this.bottomPositions = [];
        this.currentQuoteIndex = 0;
        this.quoteRotationInterval = null;
        this.factRotationInterval = null;
        this.currentFontSize = 110;
        this.showKnowledgePanelEnabled = localStorage.getItem('showKnowledgePanel') !== 'false';
        
        this.memoryMode = true;
        this.memoryProjects = [];
        this.memorySessions = [];
        this.currentProjectId = null;
        this.currentSessionId = null;
        
        this.thinkerConfig = {
            freud: { name: 'Freud', emoji: '👴', color: 'freud' },
            kuczynski: { name: 'ZHI', emoji: '🤓', color: 'kuczynski' },
            jung: { name: 'Jung', emoji: '🧔', color: 'jung' },
            hume: { name: 'Hume', emoji: '🎩', color: 'hume' },
            nietzsche: { name: 'Nietzsche', emoji: '⚡', color: 'nietzsche' },
            bergler: { name: 'Bergler', emoji: '🧠', color: 'bergler' }
        };
        
        this.workLinks = {
            'ZHI': { title: 'Conceptual Atomism' },
            'EP': { title: 'Essays in Philosophy' },
            'CFACT': { title: 'Curious Facts' },
            'ANALPHIL': { title: 'Analytic Philosophy' },
            'CATOM': { title: 'Conception and Causation' },
            'KMETA': { title: 'Metaphysics & Epistemology' },
            'KEPIST': { title: 'Theoretical Knowledge' },
            'OCD': { title: 'OCD and Philosophy' },
            'DOCD': { title: 'Dialogue on OCD' },
            'ATTACH': { title: 'Attachment Theory' },
            'CHOMSKY': { title: "Chomsky's Contributions" },
            'KANT': { title: 'Kant and Hume on Induction' },
            'INTENS': { title: 'Intensionality and Modality' },
            'LOGIC': { title: 'Logic and Set Theory' },
            'MORAL': { title: 'Moral Structure of Legal Obligation' },
            'FREUD': { title: 'Works of Freud' },
            'JUNG': { title: 'Works of Jung' }
        };
        
        this.readerModal = null;
        this.createReaderModal();
        
        this.resizeHandle = document.getElementById('panel-resize-handle');
        this.dualPanelContainer = document.querySelector('.dual-panel-container');
        
        this.setupEventListeners();
        this.initPanelResize();
        this.loadPanelSizes();
        this.initInputResize();
        this.loadInputHeight();
        this.initMemoryMode();
        this.loadDatabases();
        this.loadProviders();
        this.checkSession();
        this.showWelcomeMessage();
        this.loadSavedFontSize();
        this.initTopicsFeature();
    }
    
    initPanelResize() {
        if (!this.resizeHandle || !this.dialoguePanel || !this.archivePanel) return;
        
        let isResizing = false;
        let startX = 0;
        let startDialogueWidth = 0;
        let startArchiveWidth = 0;
        
        const startResize = (e) => {
            isResizing = true;
            startX = e.clientX || e.touches[0].clientX;
            startDialogueWidth = this.dialoguePanel.offsetWidth;
            startArchiveWidth = this.archivePanel.offsetWidth;
            this.resizeHandle.classList.add('dragging');
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        };
        
        const doResize = (e) => {
            if (!isResizing) return;
            
            const clientX = e.clientX || (e.touches && e.touches[0].clientX);
            if (!clientX) return;
            
            const deltaX = clientX - startX;
            const containerWidth = this.dualPanelContainer.offsetWidth;
            
            let newDialogueWidth = startDialogueWidth + deltaX;
            let newArchiveWidth = startArchiveWidth - deltaX;
            
            const minDialogue = 300;
            const minArchive = 200;
            
            if (newDialogueWidth < minDialogue) {
                newDialogueWidth = minDialogue;
                newArchiveWidth = containerWidth - minDialogue - this.resizeHandle.offsetWidth;
            }
            if (newArchiveWidth < minArchive) {
                newArchiveWidth = minArchive;
                newDialogueWidth = containerWidth - minArchive - this.resizeHandle.offsetWidth;
            }
            
            const dialogueFlex = newDialogueWidth / containerWidth * 10;
            const archiveFlex = newArchiveWidth / containerWidth * 10;
            
            this.dialoguePanel.style.flex = dialogueFlex;
            this.archivePanel.style.flex = archiveFlex;
        };
        
        const stopResize = () => {
            if (!isResizing) return;
            isResizing = false;
            this.resizeHandle.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
            
            this.savePanelSizes();
        };
        
        this.resizeHandle.addEventListener('mousedown', startResize);
        this.resizeHandle.addEventListener('touchstart', startResize);
        
        document.addEventListener('mousemove', doResize);
        document.addEventListener('touchmove', doResize);
        
        document.addEventListener('mouseup', stopResize);
        document.addEventListener('touchend', stopResize);
    }
    
    savePanelSizes() {
        const dialogueFlex = this.dialoguePanel.style.flex || '7';
        const archiveFlex = this.archivePanel.style.flex || '3';
        localStorage.setItem('freudgpt-panel-sizes', JSON.stringify({
            dialogue: dialogueFlex,
            archive: archiveFlex
        }));
    }
    
    loadPanelSizes() {
        const saved = localStorage.getItem('freudgpt-panel-sizes');
        if (saved) {
            try {
                const sizes = JSON.parse(saved);
                if (sizes.dialogue) this.dialoguePanel.style.flex = sizes.dialogue;
                if (sizes.archive) this.archivePanel.style.flex = sizes.archive;
            } catch (e) {
                console.log('Could not load panel sizes');
            }
        }
    }
    
    initInputResize() {
        const inputResizeHandle = document.getElementById('input-resize-handle');
        const inputSection = document.getElementById('input-section');
        const dualPanelContainer = document.querySelector('.dual-panel-container');
        const workshopMain = document.querySelector('.workshop-main');
        
        if (!inputResizeHandle || !inputSection || !dualPanelContainer) return;
        
        let isResizing = false;
        let startY = 0;
        let startInputHeight = 0;
        let startPanelHeight = 0;
        
        const startResize = (e) => {
            isResizing = true;
            startY = e.clientY || e.touches[0].clientY;
            startInputHeight = inputSection.offsetHeight;
            startPanelHeight = dualPanelContainer.offsetHeight;
            inputResizeHandle.classList.add('dragging');
            document.body.style.cursor = 'row-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        };
        
        const doResize = (e) => {
            if (!isResizing) return;
            
            const clientY = e.clientY || (e.touches && e.touches[0].clientY);
            if (!clientY) return;
            
            const deltaY = clientY - startY;
            
            const minInputHeight = 180;
            const maxInputHeight = 450;
            
            let newInputHeight = startInputHeight - deltaY;
            newInputHeight = Math.max(minInputHeight, Math.min(maxInputHeight, newInputHeight));
            
            inputSection.style.height = newInputHeight + 'px';
            inputSection.style.minHeight = minInputHeight + 'px';
            inputSection.style.maxHeight = maxInputHeight + 'px';
            
            if (newInputHeight <= 200) {
                inputSection.classList.add('collapsed');
            } else {
                inputSection.classList.remove('collapsed');
            }
        };
        
        const stopResize = () => {
            if (!isResizing) return;
            isResizing = false;
            inputResizeHandle.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
            
            this.saveInputHeight();
        };
        
        inputResizeHandle.addEventListener('mousedown', startResize);
        inputResizeHandle.addEventListener('touchstart', startResize);
        
        document.addEventListener('mousemove', doResize);
        document.addEventListener('touchmove', doResize);
        
        document.addEventListener('mouseup', stopResize);
        document.addEventListener('touchend', stopResize);
    }
    
    saveInputHeight() {
        const inputSection = document.getElementById('input-section');
        if (inputSection) {
            const height = inputSection.style.height || 'auto';
            const collapsed = inputSection.classList.contains('collapsed');
            localStorage.setItem('freudgpt-input-height', JSON.stringify({ height, collapsed }));
        }
    }
    
    loadInputHeight() {
        const saved = localStorage.getItem('freudgpt-input-height');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                const inputSection = document.getElementById('input-section');
                if (inputSection && data.height && data.height !== 'auto') {
                    inputSection.style.height = data.height;
                    inputSection.style.minHeight = '180px';
                    inputSection.style.maxHeight = '450px';
                    if (data.collapsed) {
                        inputSection.classList.add('collapsed');
                    }
                }
            } catch (e) {
                console.log('Could not load input height');
            }
        }
    }
    
    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        this.userInput.addEventListener('input', () => {
            this.autoExpandTextarea();
        });

        this.userInput.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.userInput.classList.add('drag-over');
        });
        this.userInput.addEventListener('dragleave', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.userInput.classList.remove('drag-over');
        });
        this.userInput.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.userInput.classList.remove('drag-over');
            const files = Array.from(e.dataTransfer.files);
            if (files.length > 0) {
                this.handleDroppedFiles(files);
            }
        });

        const composeArea = document.querySelector('.compose-area');
        if (composeArea) {
            composeArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.userInput.classList.add('drag-over');
            });
            composeArea.addEventListener('dragleave', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.userInput.classList.remove('drag-over');
            });
            composeArea.addEventListener('drop', (e) => {
                e.preventDefault();
                e.stopPropagation();
                this.userInput.classList.remove('drag-over');
                const files = Array.from(e.dataTransfer.files);
                if (files.length > 0) {
                    this.handleDroppedFiles(files);
                }
            });
        }

        this.uploadButton.addEventListener('click', () => {
            this.openUploadModal();
        });
        
        this.fileInput.addEventListener('change', (e) => {
            if (e.target.files[0]) {
                this.handleFileUpload(e.target.files[0]);
            }
        });
        
        this.initUploadModal();
        
        this.avatarButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                this.selectThinker(btn.dataset.db);
            });
        });
        
        this.providerSelect.addEventListener('change', () => {
            this.updateModelDropdown();
        });
        
        this.answerLengthSlider.addEventListener('input', () => {
            this.answerLengthValue.textContent = this.answerLengthSlider.value;
        });
        
        this.quoteCountSlider.addEventListener('input', () => {
            this.quoteCountValue.textContent = this.quoteCountSlider.value;
        });
        
        if (this.creativitySlider) {
            this.creativitySlider.addEventListener('input', () => {
                this.creativityValue.textContent = this.creativitySlider.value;
            });
        }
        
        this.fontSizeSlider.addEventListener('input', () => {
            const size = this.fontSizeSlider.value;
            this.fontSizeValue.textContent = size + '%';
            this.applyFontSize(size);
        });
        
        document.getElementById('download-chat-btn').addEventListener('click', () => {
            this.downloadCompleteChat('txt');
        });
        
        document.getElementById('download-dialogue-btn').addEventListener('click', () => {
            this.downloadCompleteChat('txt');
        });
        
        document.getElementById('clear-chat-btn').addEventListener('click', () => {
            this.clearChat();
        });
        
        document.getElementById('close-knowledge-panel').addEventListener('click', () => {
            this.hideKnowledgePanel();
        });

        const knowledgePanelToggle = document.getElementById('knowledge-panel-toggle');
        if (knowledgePanelToggle) {
            knowledgePanelToggle.checked = this.showKnowledgePanelEnabled;
            knowledgePanelToggle.addEventListener('change', (e) => {
                this.showKnowledgePanelEnabled = e.target.checked;
                localStorage.setItem('showKnowledgePanel', e.target.checked);
                if (!e.target.checked) this.hideKnowledgePanel();
            });
        }
        
        this.archiveFontSize = 100;
        document.getElementById('archive-font-down').addEventListener('click', () => {
            this.adjustArchiveFontSize(-10);
        });
        document.getElementById('archive-font-up').addEventListener('click', () => {
            this.adjustArchiveFontSize(10);
        });
        this.loadArchiveFontSize();

        const toggleArchiveBtn = document.getElementById('toggle-archive-btn');
        const archivePanel = document.getElementById('archive-panel');
        const resizeHandle = document.getElementById('panel-resize-handle');
        if (toggleArchiveBtn && archivePanel) {
            if (localStorage.getItem('freudgpt-archive-collapsed') === 'true') {
                archivePanel.classList.add('collapsed');
                if (resizeHandle) resizeHandle.style.display = 'none';
                toggleArchiveBtn.textContent = '▶';
                toggleArchiveBtn.title = 'Expand Archive';
            }
            toggleArchiveBtn.addEventListener('click', () => {
                const isCollapsed = archivePanel.classList.toggle('collapsed');
                if (resizeHandle) resizeHandle.style.display = isCollapsed ? 'none' : '';
                toggleArchiveBtn.textContent = isCollapsed ? '▶' : '◀';
                toggleArchiveBtn.title = isCollapsed ? 'Expand Archive' : 'Collapse Archive';
                localStorage.setItem('freudgpt-archive-collapsed', isCollapsed);
            });
        }
    }
    
    hideKnowledgePanel() {
        this.knowledgePanel.style.display = 'none';
        if (this.quoteRotationInterval) {
            clearInterval(this.quoteRotationInterval);
            this.quoteRotationInterval = null;
        }
        if (this.factRotationInterval) {
            clearInterval(this.factRotationInterval);
            this.factRotationInterval = null;
        }
    }
    
    adjustArchiveFontSize(delta) {
        this.archiveFontSize = Math.max(50, Math.min(150, this.archiveFontSize + delta));
        document.getElementById('archive-font-size').textContent = this.archiveFontSize + '%';
        this.applyArchiveFontSize();
        localStorage.setItem('freudgpt-archive-font-size', this.archiveFontSize);
    }
    
    applyArchiveFontSize() {
        const scale = this.archiveFontSize / 100;
        const baseFontSize = 0.7 * scale;
        document.querySelectorAll('.quote-text').forEach(el => {
            el.style.fontSize = baseFontSize + 'em';
        });
        document.querySelectorAll('.source-text').forEach(el => {
            el.style.fontSize = (0.75 * scale) + 'em';
        });
    }
    
    loadArchiveFontSize() {
        const saved = localStorage.getItem('freudgpt-archive-font-size');
        if (saved) {
            this.archiveFontSize = parseInt(saved);
            document.getElementById('archive-font-size').textContent = this.archiveFontSize + '%';
            this.applyArchiveFontSize();
        }
    }
    
    selectThinker(database) {
        this.selectedDatabase = database;
        this.avatarButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.db === database);
        });
        if (this.memoryMode) {
            this.currentProjectId = null;
            this.currentSessionId = null;
            this.loadMemoryProjects();
        }
    }
    
    applyFontSize(sizePercent) {
        this.currentFontSize = parseInt(sizePercent);
        const scale = sizePercent / 100;
        const dialogueFontSize = (1.0 * scale) + 'em';
        const archiveFontSize = (0.85 * scale) + 'em';
        const archiveIdSize = (0.7 * scale) + 'em';
        
        document.querySelectorAll('.message-text').forEach(el => {
            el.style.fontSize = dialogueFontSize;
        });
        
        document.querySelectorAll('.source-text').forEach(el => {
            el.style.fontSize = archiveFontSize;
        });
        
        document.querySelectorAll('.source-id').forEach(el => {
            el.style.fontSize = archiveIdSize;
        });
        
        localStorage.setItem('freudgpt-font-size', sizePercent);
    }
    
    getCurrentDialogueFontSize() {
        const scale = this.currentFontSize / 100;
        return (1.0 * scale) + 'em';
    }
    
    loadSavedFontSize() {
        const saved = localStorage.getItem('freudgpt-font-size');
        const fontSize = saved || '110';
        this.fontSizeSlider.value = fontSize;
        this.fontSizeValue.textContent = fontSize + '%';
        this.applyFontSize(fontSize);
    }
    
    async loadDatabases() {
        try {
            const response = await fetch('/api/databases');
            const data = await response.json();
            this.databases = data.databases;
            this.updateAvatarCounts();
            this.updateFooterStats();
        } catch (error) {
            console.error('Failed to load databases:', error);
        }
    }
    
    updateAvatarCounts() {
        this.databases.forEach(db => {
            const baseId = db.id === 'kuczynski' ? 'zhi' : db.id;
            const countEl = document.getElementById(`${baseId}-count`);
            if (countEl) {
                countEl.textContent = db.count.toLocaleString();
            }
            const headerCountEl = document.getElementById(`${baseId}-count-header`);
            if (headerCountEl) {
                headerCountEl.textContent = db.count.toLocaleString();
            }
        });
    }
    
    updateFooterStats() {
        const totalPositions = this.databases.reduce((sum, db) => sum + db.count, 0);
        document.getElementById('footer-stats').textContent = 
            `Powered by ${totalPositions.toLocaleString()} philosophical positions from Freud, ZHI, Jung, Hume & Nietzsche`;
    }
    
    async loadProviders() {
        try {
            const response = await fetch('/api/providers');
            const data = await response.json();
            this.providers = data.providers;
            this.updateProviderDropdown();
        } catch (error) {
            console.error('Failed to load providers:', error);
            this.providerSelect.innerHTML = '<option value="">No providers available</option>';
        }
    }
    
    updateProviderDropdown() {
        if (this.providers.length === 0) {
            this.providerSelect.innerHTML = '<option value="">No providers configured</option>';
            return;
        }
        
        this.providerSelect.innerHTML = this.providers.map(p => 
            `<option value="${p.id}" ${p.default ? 'selected' : ''}>${p.name}</option>`
        ).join('');
        
        this.updateModelDropdown();
    }
    
    updateModelDropdown() {
        const selectedProvider = this.providers.find(p => p.id === this.providerSelect.value);
        if (!selectedProvider) {
            this.modelSelect.innerHTML = '<option value="">Default</option>';
            return;
        }
        
        this.modelSelect.innerHTML = '<option value="">Default</option>' + 
            selectedProvider.models.map(m => 
                `<option value="${m}">${m}</option>`
            ).join('');
    }
    
    autoExpandTextarea() {
        this.userInput.style.height = 'auto';
        const newHeight = Math.min(this.userInput.scrollHeight, 200);
        this.userInput.style.height = newHeight + 'px';
    }
    
    async checkSession() {
        try {
            const response = await fetch('/api/check-session');
            const data = await response.json();
            if (data.logged_in) {
                this.updateUserStatus(data.username, data.picture);
            } else {
                this.updateUserStatus(null);
            }
        } catch (error) {
            console.error('Session check failed:', error);
        }
    }
    
    updateUserStatus(username, picture) {
        if (username) {
            const avatar = picture
                ? `<img src="${picture}" alt="" class="user-avatar" referrerpolicy="no-referrer">`
                : '';
            this.userStatus.innerHTML = `
                ${avatar}
                <span>Welcome, ${username}</span>
                <button class="btn-link" onclick="workshop.logout()">Logout</button>
            `;
        } else {
            this.userStatus.innerHTML = `
                <button class="btn-link" onclick="workshop.showLoginModal()">Login</button>
            `;
        }
    }
    
    async showLoginModal() {
        const modal = document.getElementById('login-modal');
        const usernameInput = document.getElementById('username-input');
        const submitBtn = document.getElementById('login-submit-btn');
        const cancelBtn = document.getElementById('login-cancel-btn');

        try {
            const resp = await fetch('/api/check-session');
            const data = await resp.json();
            const googleBtn = document.getElementById('google-login-btn');
            const divider = document.querySelector('#login-modal .login-divider');
            const show = !!data.google_login_available;
            if (googleBtn) googleBtn.style.display = show ? 'flex' : 'none';
            if (divider) divider.style.display = show ? 'flex' : 'none';
        } catch (e) { /* leave button as-is on error */ }

        modal.style.display = 'flex';
        usernameInput.value = '';
        usernameInput.focus();
        
        const handleSubmit = async () => {
            const username = usernameInput.value.trim();
            if (username) {
                try {
                    const response = await fetch('/api/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({username})
                    });
                    if (response.ok) {
                        modal.style.display = 'none';
                        this.updateUserStatus(username);
                    }
                } catch (error) {
                    console.error('Login failed:', error);
                }
            }
        };
        
        submitBtn.onclick = handleSubmit;
        cancelBtn.onclick = () => modal.style.display = 'none';
        usernameInput.onkeypress = (e) => {
            if (e.key === 'Enter') handleSubmit();
        };
    }
    
    async logout() {
        try {
            await fetch('/api/logout', {method: 'POST'});
            this.updateUserStatus(null);
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }
    
    async handleFileUpload(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        this.uploadButton.disabled = true;
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (data.text) {
                this.userInput.value = data.text;
                this.autoExpandTextarea();
                this.userInput.focus();
            } else if (data.error) {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error uploading file: ' + error.message);
        } finally {
            this.uploadButton.disabled = false;
            this.fileInput.value = '';
        }
    }
    
    showWelcomeMessage() {
        if (this.messageContainer.children.length === 0) {
            const welcomeDiv = document.createElement('div');
            welcomeDiv.className = 'empty-state';
            welcomeDiv.innerHTML = `
                <h2>Welcome to the Workshop</h2>
                <p>Select a thinker below, then pose your question. Watch as their thoughts unfold in The Dialogue while original source texts appear in The Archive.</p>
            `;
            this.messageContainer.appendChild(welcomeDiv);
        }
    }
    
    async fetchKnowledgeContent(database) {
        try {
            const response = await fetch(`/api/random-quotes?database=${database}&count=8`);
            const data = await response.json();
            this.knowledgeQuotes = data.quotes || [];
            this.bottomPositions = data.positions || [];
            this.bottomPositionIndex = 0;
            return true;
        } catch (error) {
            console.error('Failed to fetch knowledge content:', error);
            return false;
        }
    }
    
    showKnowledgePanel(database) {
        if (!this.knowledgePanel) return;
        
        this.knowledgePanel.className = 'knowledge-panel';
        this.knowledgePanel.classList.add(`${database}-theme`);
        
        const config = this.thinkerConfig[database] || this.thinkerConfig.freud;
        
        const headerIcon = this.knowledgePanel.querySelector('.knowledge-icon');
        const headerTitle = this.knowledgePanel.querySelector('.knowledge-title');
        if (headerIcon) headerIcon.textContent = '📚';
        if (headerTitle) headerTitle.textContent = `From ${config.name}'s Archives`;
        
        this.currentQuoteIndex = 0;
        this.updateQuoteDisplay();
        this.updateFactDisplay();
        this.updateProgressDots();
        
        this.knowledgePanel.style.display = 'block';
        
        this.startQuoteRotation();
        this.startFactRotation();
    }
    
    updateQuoteDisplay() {
        const carousel = this.knowledgePanel.querySelector('.quote-carousel');
        if (!carousel) return;
        
        if (this.knowledgeQuotes.length === 0) {
            carousel.innerHTML = '';
            return;
        }
        
        const quote = this.knowledgeQuotes[this.currentQuoteIndex];
        
        carousel.innerHTML = `
            <div class="quote-card active">
                <div class="quote-text">${quote.text}</div>
            </div>
        `;
    }
    
    updateFactDisplay() {
        const factText = this.knowledgePanel.querySelector('.fact-text');
        const factYear = this.knowledgePanel.querySelector('.fact-year');
        
        if (!this.bottomPositions || this.bottomPositions.length === 0) {
            if (factText) factText.textContent = '';
            if (factYear) factYear.style.display = 'none';
            return;
        }
        
        this.bottomPositionIndex = (this.bottomPositionIndex || 0) + 1;
        if (this.bottomPositionIndex >= this.bottomPositions.length) {
            this.bottomPositionIndex = 0;
        }
        
        const position = this.bottomPositions[this.bottomPositionIndex];
        
        if (factText) factText.textContent = position.text;
        if (factYear) factYear.style.display = 'none';
    }
    
    updateProgressDots() {
        const dotsContainer = this.knowledgePanel.querySelector('.progress-dots');
        if (!dotsContainer) return;
        
        dotsContainer.innerHTML = this.knowledgeQuotes.map((_, i) => 
            `<div class="progress-dot ${i === this.currentQuoteIndex ? 'active' : ''}"></div>`
        ).join('');
    }
    
    startQuoteRotation() {
        if (this.quoteRotationInterval) clearInterval(this.quoteRotationInterval);
        
        this.quoteRotationInterval = setInterval(async () => {
            if (this.knowledgeQuotes.length > 1) {
                this.currentQuoteIndex++;
                
                if (this.currentQuoteIndex >= this.knowledgeQuotes.length) {
                    const database = this.selectedDatabase || 'freud';
                    await this.fetchMoreQuotes(database);
                }
                
                if (this.currentQuoteIndex < this.knowledgeQuotes.length) {
                    this.updateQuoteDisplay();
                    this.updateProgressDots();
                }
            }
        }, 4000);
    }
    
    async fetchMoreQuotes(database) {
        try {
            const existingIds = this.knowledgeQuotes.map(q => q.id).join(',');
            const response = await fetch(`/api/random-quotes?database=${database}&count=8&exclude=${encodeURIComponent(existingIds)}`);
            const data = await response.json();
            if (data.quotes && data.quotes.length > 0) {
                this.knowledgeQuotes = [...this.knowledgeQuotes, ...data.quotes];
            }
        } catch (error) {
            console.log('Could not fetch more quotes');
        }
    }
    
    startFactRotation() {
        if (this.factRotationInterval) clearInterval(this.factRotationInterval);
        
        this.factRotationInterval = setInterval(() => {
            this.updateFactDisplay();
        }, 1500);
    }
    
    hideKnowledgePanel() {
        if (!this.knowledgePanel) return;
        
        if (this.quoteRotationInterval) {
            clearInterval(this.quoteRotationInterval);
            this.quoteRotationInterval = null;
        }
        if (this.factRotationInterval) {
            clearInterval(this.factRotationInterval);
            this.factRotationInterval = null;
        }
        
        this.knowledgePanel.classList.add('hiding');
        setTimeout(() => {
            this.knowledgePanel.style.display = 'none';
            this.knowledgePanel.classList.remove('hiding');
        }, 300);
    }
    
    displaySources(sources) {
        if (!this.sourcesDisplay) return;
        
        if (!sources || sources.length === 0) {
            this.sourcesDisplay.innerHTML = `
                <div class="archive-placeholder">
                    <div class="placeholder-icon">📖</div>
                    <p>No sources available for this response</p>
                </div>
            `;
            return;
        }
        
        const sourceIcons = ['📜', '📄', '📖', '📝', '🗒️'];
        
        this.sourcesDisplay.innerHTML = sources.map((source, index) => `
            <div class="source-item" data-index="${index}">
                <div class="source-header">
                    <span class="source-icon">${sourceIcons[index % sourceIcons.length]}</span>
                    <span class="source-id">${source.id || `Source ${index + 1}`}</span>
                </div>
                <div class="source-text">${source.text}</div>
            </div>
        `).join('');
        
        this.sourcesDisplay.querySelectorAll('.source-item').forEach(item => {
            item.addEventListener('click', () => {
                document.querySelectorAll('.source-item').forEach(i => i.classList.remove('highlighted'));
                item.classList.add('highlighted');
            });
        });
    }
    
    async sendMessage() {
        const question = this.userInput.value.trim();
        if (!question) return;
        
        const welcomeMsg = this.messageContainer.querySelector('.empty-state');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
        
        this.addUserMessage(question);
        this.userInput.value = '';
        this.userInput.style.height = 'auto';
        
        this.sendButton.disabled = true;
        this.uploadButton.disabled = true;
        
        const database = this.selectedDatabase;
        
        await this.fetchKnowledgeContent(database);
        if (this.showKnowledgePanelEnabled) {
            this.showKnowledgePanel(database);
        }
        
        this.sourcesDisplay.innerHTML = `
            <div class="archive-placeholder">
                <div class="placeholder-icon" style="animation: pulse-icon 1.5s infinite;">📚</div>
                <p>Searching the archives...</p>
            </div>
        `;
        
        const responseDiv = this.addAssistantMessage(database, '', true);
        const textDiv = responseDiv.querySelector('.message-text');
        const sourcesDiv = responseDiv.querySelector('.message-sources');
        
        textDiv.innerHTML = this.createThinkingAnimation(database);
        let firstToken = true;
        this.currentSources = [];
        
        try {
            const provider = this.providerSelect.value || 'anthropic';
            const model = this.modelSelect.value || '';
            const creativityLevel = parseInt(this.creativitySlider?.value) || 10;
            const enhancedMode = creativityLevel >= 11;
            const answerLength = parseInt(this.answerLengthSlider.value) || 100;
            const quoteCount = parseInt(this.quoteCountSlider.value) || 5;
            const responseMode = this.responseModeSelect?.value || 'standard';
            const dataSource = this.dataSourceSelect?.value || 'classic';
            const elevenlabsMode = !!document.getElementById('elevenlabs-mode-toggle')?.checked;
            
            const isMemoryMode = this.memoryMode && this.currentProjectId && this.currentSessionId;
            const endpoint = isMemoryMode ? '/api/memory/ask' : '/api/ask';
            const payload = {
                question,
                database,
                provider,
                model,
                enhanced_mode: enhancedMode,
                creativity_level: creativityLevel,
                answer_length: answerLength,
                quote_count: quoteCount,
                response_mode: responseMode,
                data_source: dataSource,
                elevenlabs_mode: elevenlabsMode
            };
            if (isMemoryMode) {
                payload.project_id = this.currentProjectId;
                payload.session_id = this.currentSessionId;
            }
            
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                throw new Error('Failed to get response from server');
            }
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            
            while (true) {
                const {done, value} = await reader.read();
                if (done) break;
                
                buffer += decoder.decode(value, {stream: true});
                const lines = buffer.split('\n');
                buffer = lines.pop();
                
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        try {
                            const data = JSON.parse(line.slice(6));
                            
                            if (data.type === 'resumed') {
                                // Handle resumed response from database
                                console.log(`Resuming from ${data.word_count} words`);
                                textDiv.innerHTML = '';
                                textDiv.classList.add('streaming');
                                textDiv.textContent = data.data;
                                firstToken = false;
                                this.scrollToBottom();
                            } else if (data.type === 'token') {
                                if (firstToken) {
                                    textDiv.innerHTML = '';
                                    textDiv.classList.add('streaming');
                                    firstToken = false;
                                }
                                textDiv.textContent += data.data;
                                this.scrollToBottom();
                            } else if (data.type === 'sources') {
                                const sourceIds = data.data;
                                const workLinks = this.getWorkLinks(sourceIds, database);
                                sourcesDiv.innerHTML = '📚 Sources: ' + workLinks;
                                
                                if (data.positions) {
                                    this.currentSources = data.positions;
                                    this.displaySources(data.positions);
                                }
                            } else if (data.type === 'retrieval_log') {
                                const meta = data.data;
                                const logHtml = `<div class="retrieval-log">
                                    <strong>Retrieval Log:</strong> Scanned ${meta.total_positions_scanned.toLocaleString()} positions | 
                                    ${meta.positions_above_threshold} above threshold (${(meta.threshold * 100).toFixed(0)}%) | 
                                    Max similarity: ${(meta.max_similarity * 100).toFixed(1)}% | 
                                    Mean: ${(meta.mean_similarity * 100).toFixed(1)}% | 
                                    Using top ${meta.top_k_used} | 
                                    Domains: ${meta.domains_in_results ? meta.domains_in_results.slice(0, 5).join(', ') : 'N/A'}
                                </div>`;
                                sourcesDiv.insertAdjacentHTML('beforeend', logHtml);
                                console.log('Retrieval metadata:', meta);
                            } else if (data.type === 'done') {
                                textDiv.classList.remove('streaming');
                                // ElevenLabs post-process: sanitize and replace text BEFORE counting words
                                if (elevenlabsMode) {
                                    const cleaned = this.toElevenLabsFormat(textDiv.textContent || '');
                                    if (cleaned) {
                                        textDiv.textContent = cleaned;
                                        this.addElevenLabsAffordances(responseDiv, cleaned);
                                    }
                                }
                                const wordCount = (textDiv.textContent || '').trim().split(/\s+/).filter(w => w.length > 0).length;
                                const wcBadge = document.createElement('div');
                                wcBadge.className = 'word-count-badge';
                                wcBadge.textContent = `${wordCount.toLocaleString()} words`;
                                textDiv.parentNode.insertBefore(wcBadge, textDiv.nextSibling);
                                this.addDownloadButton(responseDiv, question);
                                this.hideKnowledgePanel();
                            }
                        } catch (e) {
                            console.error('Error parsing SSE data:', e);
                        }
                    }
                }
            }
        } catch (error) {
            textDiv.textContent = 'Error: ' + error.message;
            textDiv.classList.remove('streaming');
            this.hideKnowledgePanel();
        } finally {
            this.sendButton.disabled = false;
            this.uploadButton.disabled = false;
        }
    }
    
    getWorkLinks(sourceIds, database) {
        const seenWorks = new Set();
        const links = [];
        
        for (const id of sourceIds) {
            let workPrefix = id.split('-')[0];
            if (database === 'freud' || database.startsWith('freud')) {
                workPrefix = 'FREUD';
            } else if (database === 'jung') {
                workPrefix = 'JUNG';
            }
            
            if (seenWorks.has(workPrefix)) continue;
            seenWorks.add(workPrefix);
            
            const work = this.workLinks[workPrefix];
            if (work) {
                links.push(`<a href="#" class="source-link" onclick="workshop.openReader('${workPrefix}'); return false;">${work.title}</a>`);
            }
        }
        
        return links.length > 0 ? links.join(', ') : sourceIds.slice(0, 3).join(', ');
    }
    
    createReaderModal() {
        this.readerModal = document.createElement('div');
        this.readerModal.id = 'reader-modal';
        this.readerModal.className = 'reader-modal';
        this.readerModal.innerHTML = `
            <div class="reader-container">
                <div class="reader-header">
                    <h2 class="reader-title">Loading...</h2>
                    <div class="reader-controls">
                        <button class="reader-btn" id="reader-font-decrease">A-</button>
                        <button class="reader-btn" id="reader-font-increase">A+</button>
                        <button class="reader-close" id="reader-close">&times;</button>
                    </div>
                </div>
                <div class="reader-search">
                    <input type="text" id="reader-search-input" placeholder="Search in text...">
                    <button class="reader-btn" id="reader-search-btn">Find</button>
                    <span id="reader-search-count"></span>
                </div>
                <div class="reader-content" id="reader-content">
                    <div class="reader-loading">Loading work...</div>
                </div>
            </div>
        `;
        document.body.appendChild(this.readerModal);
        
        document.getElementById('reader-close').addEventListener('click', () => this.closeReader());
        document.getElementById('reader-font-increase').addEventListener('click', () => this.adjustReaderFont(1.1));
        document.getElementById('reader-font-decrease').addEventListener('click', () => this.adjustReaderFont(0.9));
        document.getElementById('reader-search-btn').addEventListener('click', () => this.searchInReader());
        document.getElementById('reader-search-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchInReader();
        });
        
        this.readerModal.addEventListener('click', (e) => {
            if (e.target === this.readerModal) this.closeReader();
        });
        
        this.readerFontSize = 1.1;
    }
    
    async openReader(workId, searchText = null) {
        this.readerModal.style.display = 'flex';
        const content = document.getElementById('reader-content');
        const title = document.getElementById('reader-title');
        
        content.innerHTML = '<div class="reader-loading">Loading work...</div>';
        
        try {
            const response = await fetch(`/api/work/${workId}`);
            const data = await response.json();
            
            if (data.error) {
                content.innerHTML = `<div class="reader-error">Work not available: ${data.error}</div>`;
                return;
            }
            
            document.querySelector('.reader-title').textContent = data.title;
            
            const formattedText = data.text
                .split('\n\n')
                .map(p => `<p>${this.escapeHtml(p)}</p>`)
                .join('');
            
            content.innerHTML = formattedText;
            content.style.fontSize = `${this.readerFontSize}em`;
            
            if (searchText) {
                document.getElementById('reader-search-input').value = searchText;
                this.searchInReader();
            }
        } catch (error) {
            content.innerHTML = `<div class="reader-error">Error loading work: ${error.message}</div>`;
        }
    }
    
    closeReader() {
        this.readerModal.style.display = 'none';
    }
    
    adjustReaderFont(factor) {
        this.readerFontSize *= factor;
        this.readerFontSize = Math.max(0.8, Math.min(2.5, this.readerFontSize));
        document.getElementById('reader-content').style.fontSize = `${this.readerFontSize}em`;
    }
    
    searchInReader() {
        const searchText = document.getElementById('reader-search-input').value.trim();
        if (!searchText) return;
        
        const content = document.getElementById('reader-content');
        const text = content.innerHTML;
        
        const cleanText = text.replace(/<mark[^>]*>(.*?)<\/mark>/gi, '$1');
        
        const regex = new RegExp(`(${searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        const highlighted = cleanText.replace(regex, '<mark class="search-highlight">$1</mark>');
        
        content.innerHTML = highlighted;
        
        const matches = content.querySelectorAll('.search-highlight');
        document.getElementById('reader-search-count').textContent = `${matches.length} found`;
        
        if (matches.length > 0) {
            matches[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }
    
    createThinkingAnimation(database) {
        const config = this.thinkerConfig[database] || this.thinkerConfig.freud;
        
        // Get position statements for scrolling marquee
        const positions = this.bottomPositions || [];
        const marqueeStatements = positions.slice(0, 20).map(p => 
            `<div class="position-statement">${this.escapeHtml(p.text)}</div>`
        ).join('');
        
        // Duplicate for seamless loop
        const doubledStatements = marqueeStatements + marqueeStatements;
        
        return `
            <div class="thinking-animation">
                <div class="orbit-container">
                    <div class="sun"></div>
                    <div class="orbit-path">
                        <div class="freud-head">${config.emoji}</div>
                    </div>
                </div>
                <div class="thinking-text">${config.name} is contemplating...</div>
                <div class="position-marquee">
                    <div class="position-marquee-content">
                        ${doubledStatements || '<div class="position-statement">Loading philosophical positions...</div>'}
                    </div>
                </div>
            </div>
        `;
    }
    
    addUserMessage(content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message message-user';
        
        messageDiv.innerHTML = `
            <div class="message-bubble">
                <div class="message-text" style="font-size: ${this.getCurrentDialogueFontSize()}">${this.escapeHtml(content)}</div>
            </div>
        `;
        
        this.messageContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageDiv;
    }
    
    addAssistantMessage(database, content = '', isStreaming = false) {
        const config = this.thinkerConfig[database] || this.thinkerConfig.freud;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message message-assistant';
        
        messageDiv.innerHTML = `
            <div class="thinker-header">
                <div class="thinker-avatar ${config.color}">${config.emoji}</div>
                <span class="thinker-name">${config.name}</span>
            </div>
            <div class="message-bubble">
                <div class="message-text" style="font-size: ${this.getCurrentDialogueFontSize()}">${content}</div>
                <div class="message-sources"></div>
            </div>
        `;
        
        this.messageContainer.appendChild(messageDiv);
        this.scrollToBottom();
        
        return messageDiv;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ElevenLabs Studio expects: every non-empty line "^Speaker \d+: .+$", blank line between turns.
    // No stage directions, no markdown, no titles, no narration.
    toElevenLabsFormat(raw) {
        if (!raw) return '';
        let text = String(raw);
        // 1) Strip markdown emphasis/headings/code fences
        text = text.replace(/```[\s\S]*?```/g, ' ');
        text = text.replace(/`([^`]+)`/g, '$1');
        text = text.replace(/^\s{0,3}#{1,6}\s+.*$/gm, '');
        text = text.replace(/\*\*([^*]+)\*\*/g, '$1');
        text = text.replace(/__([^_]+)__/g, '$1');
        text = text.replace(/(?<!\*)\*(?!\*)([^*\n]+)\*(?!\*)/g, '$1');
        text = text.replace(/(?<!_)_(?!_)([^_\n]+)_(?!_)/g, '$1');
        // 2) Strip parenthetical/bracketed stage directions
        text = text.replace(/\([^)]{1,80}\)/g, ' ');
        text = text.replace(/\[[^\]]{1,80}\]/g, ' ');
        text = text.replace(/\*[^*\n]{1,80}\*/g, ' ');
        // 3) Normalize line endings, split into logical lines
        text = text.replace(/\r\n/g, '\n');
        const lines = text.split('\n').map(l => l.trim());

        // 4) Detect speaker prefixes and remap to Speaker N
        // Accepted source prefixes (case-insensitive at line start, followed by colon or em-dash):
        //   Speaker 1, Speaker1, S1, Person A, Host, Guest, Q, A, Interviewer, Interviewee, Moderator,
        //   or a CapitalizedName (1–3 tokens, no trailing punctuation other than the colon).
        const knownLabel = /^\s*(speaker\s*\d+|s\d+|person\s+[a-z]|host|guest|interviewer|interviewee|moderator|q|a|questioner|answerer)\s*[:\-—–]\s*/i;
        const nameLabel = /^\s*([A-Z][a-zA-Z'’.\-]{1,20}(?:\s+[A-Z][a-zA-Z'’.\-]{1,20}){0,2})\s*[:\-—–]\s+/;

        const speakerMap = new Map();      // raw label (lowercased) -> Speaker N
        let nextSpeakerNum = 1;
        const labelFor = (rawLabel) => {
            const key = rawLabel.toLowerCase().trim();
            // Normalize "speaker 1" / "s1" / "speaker1" → speaker1
            const norm = key.replace(/\s+/g, '');
            const speakerMatch = norm.match(/^(?:speaker|s)(\d+)$/);
            if (speakerMatch) {
                const n = parseInt(speakerMatch[1], 10);
                // Preserve original numbering if it's a low integer, otherwise auto-assign
                if (n >= 1 && n <= 9) return `Speaker ${n}`;
            }
            if (!speakerMap.has(key)) {
                speakerMap.set(key, `Speaker ${nextSpeakerNum++}`);
            }
            return speakerMap.get(key);
        };

        // 5) Walk lines: emit one turn per labelled line; lines without labels attach to the prior turn
        const turns = []; // { label: 'Speaker N', text: '' }
        for (const ln of lines) {
            if (!ln) continue;
            let m = ln.match(knownLabel);
            let rest, label;
            if (m) {
                label = labelFor(m[1]);
                rest = ln.slice(m[0].length).trim();
            } else {
                m = ln.match(nameLabel);
                if (m) {
                    label = labelFor(m[1]);
                    rest = ln.slice(m[0].length).trim();
                } else {
                    // Continuation — append to last turn if we have one
                    if (turns.length > 0) {
                        turns[turns.length - 1].text += ' ' + ln;
                    }
                    // Else: orphaned narration before first speaker — discard
                    continue;
                }
            }
            // Strip any residual leading punctuation/whitespace
            rest = rest.replace(/^[\s\-—–:]+/, '').trim();
            if (rest) turns.push({ label, text: rest });
        }

        // 6) If we never detected any speakers, fall back: split into paragraphs and alternate Speaker 1/2
        if (turns.length === 0) {
            const paras = lines.filter(Boolean);
            for (let i = 0; i < paras.length; i++) {
                turns.push({ label: `Speaker ${(i % 2) + 1}`, text: paras[i] });
            }
        }

        // 7) Clean each turn's text (collapse whitespace, strip residual asterisks/quotes-of-stage-directions)
        for (const t of turns) {
            t.text = t.text.replace(/\s+/g, ' ').trim();
        }

        // 8) Build output and validate; drop any line that fails ^Speaker \d+: .+$
        const validRe = /^Speaker \d+: .+$/;
        const out = [];
        for (const t of turns) {
            const line = `${t.label}: ${t.text}`;
            if (validRe.test(line)) out.push(line);
        }
        return out.join('\n\n');
    }

    addElevenLabsAffordances(messageDiv, cleanedText) {
        // Avoid duplicating affordances if the message is re-processed
        const existing = messageDiv.querySelector('.elevenlabs-affordances');
        if (existing) existing.remove();

        const bubble = messageDiv.querySelector('.message-bubble') || messageDiv;
        const wrap = document.createElement('div');
        wrap.className = 'elevenlabs-affordances';
        wrap.style.cssText = 'margin-top:10px;padding:10px 12px;background:#F0FDFA;border:1px solid #0F766E22;border-radius:8px;display:flex;flex-direction:column;gap:8px;';

        const btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:8px;flex-wrap:wrap;';

        const copyBtn = document.createElement('button');
        copyBtn.type = 'button';
        copyBtn.textContent = '📋 Copy to Clipboard';
        copyBtn.style.cssText = 'padding:6px 12px;background:#0F766E;color:white;border:none;border-radius:6px;cursor:pointer;font-size:0.9em;';
        copyBtn.addEventListener('click', async () => {
            try {
                await navigator.clipboard.writeText(cleanedText);
                const orig = copyBtn.textContent;
                copyBtn.textContent = '✓ Copied';
                setTimeout(() => { copyBtn.textContent = orig; }, 1500);
            } catch (e) {
                // Fallback for older browsers
                const ta = document.createElement('textarea');
                ta.value = cleanedText; document.body.appendChild(ta); ta.select();
                document.execCommand('copy'); document.body.removeChild(ta);
                copyBtn.textContent = '✓ Copied';
                setTimeout(() => { copyBtn.textContent = '📋 Copy to Clipboard'; }, 1500);
            }
        });

        const dlBtn = document.createElement('button');
        dlBtn.type = 'button';
        dlBtn.textContent = '⬇️ Download as .txt';
        dlBtn.style.cssText = 'padding:6px 12px;background:#F97316;color:white;border:none;border-radius:6px;cursor:pointer;font-size:0.9em;';
        dlBtn.addEventListener('click', () => {
            // Force Unix line endings + UTF-8
            const body = cleanedText.replace(/\r\n/g, '\n');
            const blob = new Blob([body], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url; a.download = 'dialogue.txt';
            document.body.appendChild(a); a.click();
            document.body.removeChild(a);
            setTimeout(() => URL.revokeObjectURL(url), 1000);
        });

        btnRow.appendChild(copyBtn);
        btnRow.appendChild(dlBtn);

        const helper = document.createElement('div');
        helper.style.cssText = 'font-size:0.85em;color:#0F766E;font-style:italic;';
        helper.textContent = 'Paste this into ElevenLabs Studio, then assign a voice to Speaker 1 and Speaker 2.';

        wrap.appendChild(btnRow);
        wrap.appendChild(helper);
        bubble.appendChild(wrap);
    }

    addDownloadButton(messageDiv, userQuestion) {
        const bubble = messageDiv.querySelector('.message-bubble');
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'download-buttons';
        
        const copyBtn = document.createElement('button');
        copyBtn.className = 'download-btn copy-btn';
        copyBtn.textContent = '📋 Copy';
        copyBtn.onclick = () => this.copyResponseToClipboard(messageDiv, copyBtn);
        
        const downloadMdBtn = document.createElement('button');
        downloadMdBtn.className = 'download-btn';
        downloadMdBtn.textContent = '💾 Markdown';
        downloadMdBtn.onclick = () => this.downloadExchange(messageDiv, userQuestion, 'md');
        
        const downloadTxtBtn = document.createElement('button');
        downloadTxtBtn.className = 'download-btn';
        downloadTxtBtn.textContent = '💾 Text';
        downloadTxtBtn.onclick = () => this.downloadExchange(messageDiv, userQuestion, 'txt');
        
        buttonContainer.appendChild(copyBtn);
        buttonContainer.appendChild(downloadMdBtn);
        buttonContainer.appendChild(downloadTxtBtn);
        bubble.appendChild(buttonContainer);
    }
    
    async copyResponseToClipboard(messageDiv, button) {
        const assistantText = messageDiv.querySelector('.message-text').textContent;
        
        try {
            await navigator.clipboard.writeText(assistantText);
            const originalText = button.textContent;
            button.textContent = '✓ Copied!';
            button.classList.add('copied');
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('copied');
            }, 2000);
        } catch (err) {
            const textArea = document.createElement('textarea');
            textArea.value = assistantText;
            textArea.style.position = 'fixed';
            textArea.style.left = '-9999px';
            document.body.appendChild(textArea);
            textArea.select();
            try {
                document.execCommand('copy');
                const originalText = button.textContent;
                button.textContent = '✓ Copied!';
                button.classList.add('copied');
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('copied');
                }, 2000);
            } catch (e) {
                button.textContent = '✗ Failed';
                setTimeout(() => {
                    button.textContent = '📋 Copy';
                }, 2000);
            }
            document.body.removeChild(textArea);
        }
    }
    
    downloadExchange(messageDiv, userQuestion, format = 'md') {
        const assistantText = messageDiv.querySelector('.message-text').textContent;
        const sources = messageDiv.querySelector('.message-sources').textContent;
        const thinkerName = messageDiv.querySelector('.thinker-name')?.textContent || 'Thinker';
        
        const date = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        
        let content, mimeType, extension;
        
        if (format === 'txt') {
            content = `CONVERSATION WITH ${thinkerName.toUpperCase()}
Date: ${date}

================================================================================

YOU:
${userQuestion}

--------------------------------------------------------------------------------

${thinkerName.toUpperCase()}:
${assistantText}

--------------------------------------------------------------------------------

${sources}

================================================================================

Generated by FreudGPT
`;
            mimeType = 'text/plain';
            extension = 'txt';
        } else {
            content = `# Conversation with ${thinkerName}
Date: ${date}

## Exchange

**You:** ${userQuestion}

**${thinkerName}:** ${assistantText}

**${sources}**

---

*Generated by FreudGPT*
`;
            mimeType = 'text/markdown';
            extension = 'md';
        }
        
        const blob = new Blob([content], {type: mimeType});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${thinkerName.toLowerCase()}-conversation-${Date.now()}.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    scrollToBottom() {
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
    
    clearChat() {
        if (this.messageContainer.children.length === 0) {
            return;
        }
        
        const confirmClear = confirm('Clear the entire conversation?');
        if (confirmClear) {
            this.messageContainer.innerHTML = '';
            this.sourcesDisplay.innerHTML = `
                <div class="archive-placeholder">
                    <div class="placeholder-icon">📖</div>
                    <p>Source texts will appear here as the thinker responds...</p>
                    <p class="placeholder-hint">Watch the original passages that inform each answer</p>
                </div>
            `;
            this.showWelcomeMessage();
        }
    }
    
    downloadCompleteChat(format = 'md') {
        const messages = this.messageContainer.querySelectorAll('.message');
        
        if (messages.length === 0 || this.messageContainer.querySelector('.empty-state')) {
            alert('No conversation to download');
            return;
        }
        
        const exchanges = [];
        let currentExchange = null;
        
        messages.forEach(msg => {
            if (msg.classList.contains('message-user')) {
                if (currentExchange) {
                    exchanges.push(currentExchange);
                }
                currentExchange = {
                    question: msg.querySelector('.message-text').textContent,
                    answer: '',
                    sources: '',
                    thinker: ''
                };
            } else if (msg.classList.contains('message-assistant') && currentExchange) {
                currentExchange.answer = msg.querySelector('.message-text').textContent;
                const sourcesElement = msg.querySelector('.message-sources');
                currentExchange.sources = sourcesElement ? sourcesElement.textContent : '';
                currentExchange.thinker = msg.querySelector('.thinker-name')?.textContent || 'Thinker';
            }
        });
        
        if (currentExchange) {
            exchanges.push(currentExchange);
        }
        
        if (exchanges.length === 0) {
            alert('No complete exchanges to download');
            return;
        }
        
        const date = new Date().toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        let content, mimeType, extension;
        
        if (format === 'txt') {
            content = `COMPLETE WORKSHOP SESSION
Date: ${date}
Total Exchanges: ${exchanges.length}

${'='.repeat(80)}

`;
            exchanges.forEach((exchange, index) => {
                content += `EXCHANGE ${index + 1} - with ${exchange.thinker}

YOU:
${exchange.question}

${'-'.repeat(80)}

${exchange.thinker.toUpperCase()}:
${exchange.answer}

${'-'.repeat(80)}

${exchange.sources}

${'='.repeat(80)}

`;
            });
            
            content += `
Generated by FreudGPT`;
            
            mimeType = 'text/plain';
            extension = 'txt';
        } else {
            content = `# Complete Workshop Session
Date: ${date}  
Total Exchanges: ${exchanges.length}

---

`;
            exchanges.forEach((exchange, index) => {
                content += `## Exchange ${index + 1} - with ${exchange.thinker}

**You:** ${exchange.question}

**${exchange.thinker}:** ${exchange.answer}

**${exchange.sources}**

---

`;
            });
            
            content += `
*Generated by FreudGPT*`;
            
            mimeType = 'text/markdown';
            extension = 'md';
        }
        
        const blob = new Blob([content], {type: mimeType});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `workshop-session-${Date.now()}.${extension}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    initTopicsFeature() {
        const whatToAskBtn = document.getElementById('what-to-ask-btn');
        const whatToAskBtnHeader = document.getElementById('what-to-ask-btn-header');
        const topicsModal = document.getElementById('topics-modal');
        const closeTopicsBtn = document.getElementById('close-topics-modal');
        const topicsSearch = document.getElementById('topics-search');
        
        if (!topicsModal) return;
        
        if (whatToAskBtn) {
            whatToAskBtn.addEventListener('click', () => this.openTopicsModal());
        }
        if (whatToAskBtnHeader) {
            whatToAskBtnHeader.addEventListener('click', () => this.openTopicsModal());
        }
        closeTopicsBtn.addEventListener('click', () => this.closeTopicsModal());
        
        topicsModal.addEventListener('click', (e) => {
            if (e.target === topicsModal) {
                this.closeTopicsModal();
            }
        });
        
        topicsSearch.addEventListener('input', (e) => {
            this.filterTopics(e.target.value);
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && topicsModal.style.display !== 'none') {
                this.closeTopicsModal();
            }
        });
    }
    
    async openTopicsModal() {
        const topicsModal = document.getElementById('topics-modal');
        const thinkerNameEl = document.getElementById('topics-thinker-name');
        const topicsContent = document.getElementById('topics-content');
        const topicsSearch = document.getElementById('topics-search');
        
        const thinkerNames = {
            'freud': 'Freud',
            'kuczynski': 'ZHI',
            'jung': 'Jung',
            'hume': 'Hume',
            'nietzsche': 'Nietzsche'
        };
        
        thinkerNameEl.textContent = thinkerNames[this.selectedDatabase] || this.selectedDatabase;
        topicsContent.innerHTML = '<div class="topics-loading">Loading topics...</div>';
        topicsSearch.value = '';
        topicsModal.style.display = 'flex';
        
        try {
            const response = await fetch(`/api/topics/${this.selectedDatabase}`);
            const data = await response.json();
            
            if (data.error) {
                topicsContent.innerHTML = `<div class="topics-loading">${data.error}</div>`;
                return;
            }
            
            this.currentTopicsData = data;
            this.renderTopics(data.topics);
        } catch (error) {
            console.error('Failed to load topics:', error);
            topicsContent.innerHTML = '<div class="topics-loading">Failed to load topics. Please try again.</div>';
        }
    }
    
    closeTopicsModal() {
        const topicsModal = document.getElementById('topics-modal');
        topicsModal.style.display = 'none';
    }
    
    renderTopics(topics) {
        const topicsContent = document.getElementById('topics-content');
        
        if (!topics || topics.length === 0) {
            topicsContent.innerHTML = `
                <div class="topics-no-results">
                    <div class="no-results-icon">📭</div>
                    <p>No topics available for this thinker yet.</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        topics.forEach((topic, index) => {
            html += `
                <div class="topic-card" data-topic-id="${topic.id}" data-topic-name="${this.escapeHtml(topic.name)}">
                    <div class="topic-header">
                        <div class="topic-header-left">
                            <div class="topic-number">${index + 1}</div>
                            <div class="topic-info">
                                <h3 class="topic-name">${this.escapeHtml(topic.name)}</h3>
                                <p class="topic-description">${this.escapeHtml(topic.description || '')}</p>
                            </div>
                        </div>
                        <button class="topic-ask-btn">Ask</button>
                        <div class="topic-toggle">▼</div>
                    </div>
                    <div class="topic-questions">
                        <ul class="question-list">
                            ${topic.questions.map(q => `
                                <li class="question-item" data-question="${this.escapeHtml(q)}">
                                    ${this.escapeHtml(q)}
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            `;
        });
        
        topicsContent.innerHTML = html;
        this.attachTopicEventListeners();
    }
    
    attachTopicEventListeners() {
        document.querySelectorAll('.topic-header').forEach(header => {
            header.addEventListener('click', (e) => {
                if (e.target.classList.contains('topic-ask-btn')) return;
                const topicId = header.closest('.topic-card').dataset.topicId;
                this.toggleTopic(topicId);
            });
        });
        
        document.querySelectorAll('.topic-ask-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const topicName = btn.closest('.topic-card').dataset.topicName;
                this.selectTopic(topicName);
            });
        });
        
        document.querySelectorAll('.question-item').forEach(item => {
            item.addEventListener('click', () => {
                const questionText = item.dataset.question;
                this.selectQuestion(questionText);
            });
        });
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    toggleTopic(topicId) {
        const topicCard = document.querySelector(`.topic-card[data-topic-id="${topicId}"]`);
        if (topicCard) {
            topicCard.classList.toggle('expanded');
        }
    }
    
    selectTopic(topicName) {
        this.userInput.value = `Tell me about ${topicName}`;
        this.closeTopicsModal();
        this.autoExpandTextarea();
        this.sendMessage();
    }
    
    selectQuestion(questionText) {
        this.userInput.value = questionText;
        this.closeTopicsModal();
        this.autoExpandTextarea();
        this.sendMessage();
    }
    
    filterTopics(searchText) {
        if (!this.currentTopicsData?.topics) return;
        
        const searchLower = searchText.toLowerCase().trim();
        
        if (!searchLower) {
            this.renderTopics(this.currentTopicsData.topics);
            return;
        }
        
        const filteredTopics = this.currentTopicsData.topics
            .map(topic => {
                const nameMatch = topic.name.toLowerCase().includes(searchLower);
                const descMatch = (topic.description || '').toLowerCase().includes(searchLower);
                const matchingQuestions = topic.questions.filter(q => 
                    q.toLowerCase().includes(searchLower)
                );
                
                if (nameMatch || descMatch || matchingQuestions.length > 0) {
                    return {
                        ...topic,
                        questions: matchingQuestions.length > 0 ? matchingQuestions : topic.questions
                    };
                }
                return null;
            })
            .filter(Boolean);
        
        if (filteredTopics.length === 0) {
            document.getElementById('topics-content').innerHTML = `
                <div class="topics-no-results">
                    <div class="no-results-icon">🔍</div>
                    <p>No topics or questions match "${this.escapeHtml(searchText)}"</p>
                </div>
            `;
        } else {
            this.renderTopics(filteredTopics);
            filteredTopics.forEach(topic => {
                const card = document.querySelector(`.topic-card[data-topic-id="${topic.id}"]`);
                if (card) card.classList.add('expanded');
            });
        }
    }
    initUploadModal() {
        this.uploadModal = document.getElementById('upload-modal');
        this.uploadDropzone = document.getElementById('upload-dropzone');
        this.uploadFileInput = document.getElementById('upload-file-input');
        this.uploadFileList = document.getElementById('upload-file-list');
        this.uploadProgress = document.getElementById('upload-progress');
        this.uploadProgressFill = document.getElementById('upload-progress-fill');
        this.uploadStatus = document.getElementById('upload-status');
        this.uploadSubmitBtn = document.getElementById('upload-submit-btn');
        this.uploadAuthorSelect = document.getElementById('upload-author-select');
        this.uploadType = 'arguments';
        this.uploadFiles = [];
        
        if (!this.uploadModal) return;
        
        document.getElementById('close-upload-modal')?.addEventListener('click', () => this.closeUploadModal());
        document.getElementById('upload-cancel-btn')?.addEventListener('click', () => this.closeUploadModal());
        
        document.querySelectorAll('.upload-type-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.upload-type-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.uploadType = btn.dataset.type;
            });
        });
        
        this.uploadDropzone?.addEventListener('click', () => this.uploadFileInput?.click());
        
        this.uploadDropzone?.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.uploadDropzone.classList.add('drag-over');
        });
        
        this.uploadDropzone?.addEventListener('dragleave', () => {
            this.uploadDropzone.classList.remove('drag-over');
        });
        
        this.uploadDropzone?.addEventListener('drop', (e) => {
            e.preventDefault();
            this.uploadDropzone.classList.remove('drag-over');
            const files = Array.from(e.dataTransfer.files);
            this.addFilesToUpload(files);
        });
        
        this.uploadFileInput?.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);
            this.addFilesToUpload(files);
            e.target.value = '';
        });
        
        this.uploadSubmitBtn?.addEventListener('click', () => this.submitUpload());
        
        this.uploadModal?.addEventListener('click', (e) => {
            if (e.target === this.uploadModal) this.closeUploadModal();
        });
    }
    
    async handleDroppedFiles(files) {
        const validExtensions = ['.txt', '.pdf', '.docx', '.doc'];
        const statusDiv = document.createElement('div');
        statusDiv.className = 'drop-status';
        statusDiv.textContent = 'Processing file...';
        this.userInput.parentNode.insertBefore(statusDiv, this.userInput.nextSibling);

        for (const file of files) {
            const ext = '.' + file.name.split('.').pop().toLowerCase();
            if (!validExtensions.includes(ext)) {
                statusDiv.textContent = `Unsupported: ${file.name} (use .txt, .pdf, .docx)`;
                setTimeout(() => statusDiv.remove(), 3000);
                continue;
            }

            statusDiv.textContent = `Extracting text from ${file.name}...`;

            if (ext === '.txt') {
                const text = await file.text();
                const prefix = this.userInput.value ? '\n\n' : '';
                this.userInput.value += `${prefix}[Document: ${file.name}]\n${text}`;
                this.autoExpandTextarea();
                statusDiv.textContent = `Added ${file.name} (${text.split(/\s+/).length} words)`;
                setTimeout(() => statusDiv.remove(), 3000);
            } else {
                try {
                    const formData = new FormData();
                    formData.append('file', file);
                    const res = await fetch('/api/upload', { method: 'POST', body: formData });
                    const data = await res.json();
                    if (data.text) {
                        const prefix = this.userInput.value ? '\n\n' : '';
                        this.userInput.value += `${prefix}[Document: ${file.name}]\n${data.text}`;
                        this.autoExpandTextarea();
                        statusDiv.textContent = `Added ${file.name} (${data.text.split(/\s+/).length} words)`;
                    } else {
                        statusDiv.textContent = `Failed to extract text from ${file.name}`;
                    }
                    setTimeout(() => statusDiv.remove(), 3000);
                } catch (e) {
                    statusDiv.textContent = `Error processing ${file.name}: ${e.message}`;
                    setTimeout(() => statusDiv.remove(), 3000);
                }
            }
        }
        this.userInput.focus();
    }

    openUploadModal() {
        if (!this.uploadModal) return;
        this.uploadFiles = [];
        this.renderUploadFileList();
        this.uploadProgress.style.display = 'none';
        this.uploadSubmitBtn.disabled = true;
        this.uploadModal.style.display = 'flex';
    }
    
    closeUploadModal() {
        if (this.uploadModal) {
            this.uploadModal.style.display = 'none';
        }
    }
    
    addFilesToUpload(files) {
        const validExtensions = ['.txt', '.pdf', '.docx', '.doc'];
        files.forEach(file => {
            const ext = '.' + file.name.split('.').pop().toLowerCase();
            if (validExtensions.includes(ext)) {
                if (!this.uploadFiles.find(f => f.name === file.name)) {
                    this.uploadFiles.push(file);
                }
            }
        });
        this.renderUploadFileList();
        this.uploadSubmitBtn.disabled = this.uploadFiles.length === 0;
    }
    
    removeFileFromUpload(index) {
        this.uploadFiles.splice(index, 1);
        this.renderUploadFileList();
        this.uploadSubmitBtn.disabled = this.uploadFiles.length === 0;
    }
    
    renderUploadFileList() {
        if (!this.uploadFileList) return;
        
        if (this.uploadFiles.length === 0) {
            this.uploadFileList.innerHTML = '';
            return;
        }
        
        this.uploadFileList.innerHTML = this.uploadFiles.map((file, index) => {
            const ext = file.name.split('.').pop().toLowerCase();
            const icon = ext === 'pdf' ? '📕' : ext === 'docx' || ext === 'doc' ? '📘' : '📄';
            const size = file.size > 1024 * 1024 
                ? (file.size / (1024 * 1024)).toFixed(1) + ' MB'
                : (file.size / 1024).toFixed(1) + ' KB';
            
            return `
                <div class="upload-file-item">
                    <div class="upload-file-info">
                        <span class="upload-file-icon">${icon}</span>
                        <div>
                            <div class="upload-file-name">${this.escapeHtml(file.name)}</div>
                            <div class="upload-file-size">${size}</div>
                        </div>
                    </div>
                    <button class="upload-file-remove" onclick="workshop.removeFileFromUpload(${index})">×</button>
                </div>
            `;
        }).join('');
    }
    
    async submitUpload() {
        if (this.uploadFiles.length === 0) return;
        
        this.uploadSubmitBtn.disabled = true;
        this.uploadProgress.style.display = 'block';
        this.uploadProgressFill.style.width = '0%';
        this.uploadStatus.textContent = 'Uploading...';
        
        const author = this.uploadAuthorSelect?.value || 'kuczynski';
        const type = this.uploadType;
        
        let allTexts = [];
        let totalArguments = 0;
        
        for (let i = 0; i < this.uploadFiles.length; i++) {
            const file = this.uploadFiles[i];
            const progress = ((i + 1) / this.uploadFiles.length) * 100;
            this.uploadProgressFill.style.width = progress + '%';
            this.uploadStatus.textContent = `Processing ${file.name}...`;
            
            try {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('author', author);
                formData.append('type', type);
                
                const response = await fetch('/api/upload/document', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                if (result.success) {
                    if (type === 'arguments') {
                        totalArguments += result.arguments_count || 0;
                    }
                    allTexts.push({
                        filename: file.name,
                        text: result.full_text || result.text_preview || '',
                        arguments_count: result.arguments_count || 0,
                        type: type
                    });
                }
            } catch (err) {
                console.error('Upload error:', err);
            }
        }
        
        this.uploadProgressFill.style.width = '100%';
        this.closeUploadModal();
        
        if (allTexts.length > 0) {
            this.showTextPreview(allTexts, totalArguments);
        }
    }
    
    showTextPreview(texts, totalArguments) {
        const modal = document.getElementById('text-preview-modal');
        const filenameEl = document.getElementById('preview-filename');
        const statsEl = document.getElementById('preview-stats');
        const contentEl = document.getElementById('text-preview-content');
        
        if (!modal) return;
        
        const filenames = texts.map(t => t.filename).join(', ');
        filenameEl.textContent = texts.length === 1 ? texts[0].filename : `${texts.length} Documents`;
        
        const totalChars = texts.reduce((sum, t) => sum + (t.text?.length || 0), 0);
        const totalWords = texts.reduce((sum, t) => sum + (t.text?.split(/\s+/).length || 0), 0);
        
        let statsHtml = `<span>📄 ${texts.length} file(s)</span>`;
        statsHtml += `<span>📝 ${totalWords.toLocaleString()} words</span>`;
        statsHtml += `<span>🔤 ${totalChars.toLocaleString()} characters</span>`;
        if (totalArguments > 0) {
            statsHtml += `<span>📋 ${totalArguments} arguments ingested</span>`;
        }
        statsEl.innerHTML = statsHtml;
        
        let previewHtml = '';
        texts.forEach((t, idx) => {
            if (texts.length > 1) {
                previewHtml += `\n━━━ ${t.filename} ━━━\n\n`;
            }
            previewHtml += t.text || '(No text extracted)';
            if (idx < texts.length - 1) previewHtml += '\n\n';
        });
        
        contentEl.textContent = previewHtml;
        this.currentUploadedText = previewHtml;
        
        modal.style.display = 'flex';
        
        document.getElementById('close-preview-modal')?.addEventListener('click', () => {
            modal.style.display = 'none';
        });
        document.getElementById('close-preview-btn')?.addEventListener('click', () => {
            modal.style.display = 'none';
        });
        document.getElementById('use-for-question-btn')?.addEventListener('click', () => {
            const truncated = this.currentUploadedText.substring(0, 2000);
            this.userInput.value = `Regarding this text:\n\n"${truncated}${this.currentUploadedText.length > 2000 ? '...' : ''}"\n\nWhat are your thoughts on this?`;
            modal.style.display = 'none';
            this.autoExpandTextarea();
        });
        
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.style.display = 'none';
        });
    }

    initMemoryMode() {
        const toggle = document.getElementById('memory-mode-toggle');
        const panel = document.getElementById('memory-bar');
        const projectSelect = document.getElementById('memory-project-select');
        const sessionSelect = document.getElementById('memory-session-select');
        const newProjectBtn = document.getElementById('new-project-btn');
        const deleteProjectBtn = document.getElementById('delete-project-btn');
        const newSessionBtn = document.getElementById('new-session-btn');
        const deleteSessionBtn = document.getElementById('delete-session-btn');
        const viewTractatusBtn = document.getElementById('view-tractatus-btn');
        const closeTractatusBtn = document.getElementById('close-tractatus-modal');

        if (!toggle) return;

        const savedMemoryState = localStorage.getItem('freudgpt-memory-mode');
        this.memoryMode = savedMemoryState !== 'false';
        toggle.checked = this.memoryMode;
        panel.style.display = this.memoryMode ? 'block' : 'none';
        if (this.memoryMode) this.loadMemoryProjects();

        toggle.addEventListener('change', () => {
            this.memoryMode = toggle.checked;
            localStorage.setItem('freudgpt-memory-mode', toggle.checked);
            panel.style.display = this.memoryMode ? 'block' : 'none';
            if (this.memoryMode) {
                this.loadMemoryProjects();
            } else {
                this.currentProjectId = null;
                this.currentSessionId = null;
            }
        });

        projectSelect.addEventListener('change', () => {
            this.currentProjectId = projectSelect.value ? parseInt(projectSelect.value) : null;
            this.currentSessionId = null;
            if (this.currentProjectId) {
                this.loadMemorySessions(this.currentProjectId);
            } else {
                sessionSelect.innerHTML = '<option value="">Select Session...</option>';
            }
        });

        sessionSelect.addEventListener('change', () => {
            this.currentSessionId = sessionSelect.value ? parseInt(sessionSelect.value) : null;
            if (this.currentSessionId) {
                this.loadSessionTranscript(this.currentSessionId);
            }
        });

        newProjectBtn.addEventListener('click', () => {
            const name = prompt('Project name:');
            if (name) this.createMemoryProject(name);
        });

        deleteProjectBtn.addEventListener('click', () => {
            if (this.currentProjectId && confirm('Delete this project and all its sessions?')) {
                this.deleteMemoryProject(this.currentProjectId);
            }
        });

        newSessionBtn.addEventListener('click', async () => {
            if (!this.currentProjectId) {
                await this.createMemoryProject('My Chats');
                return;
            }
            const count = (this.memorySessions ? this.memorySessions.length : 0) + 1;
            this.createMemorySession(this.currentProjectId, `Chat ${count}`);
        });

        document.getElementById('rename-session-btn').addEventListener('click', () => {
            if (this.currentSessionId) {
                const currentTitle = document.getElementById('memory-session-select').selectedOptions[0]?.textContent || '';
                const newTitle = prompt('Rename session:', currentTitle);
                if (newTitle && newTitle.trim()) {
                    this.renameMemorySession(this.currentSessionId, newTitle.trim());
                }
            }
        });

        deleteSessionBtn.addEventListener('click', () => {
            if (this.currentSessionId && confirm('Delete this session?')) {
                this.deleteMemorySession(this.currentSessionId);
            }
        });

        viewTractatusBtn.addEventListener('click', () => {
            if (this.currentProjectId) this.showTractatusTree(this.currentProjectId);
        });

        document.getElementById('download-tractatus-btn')?.addEventListener('click', () => {
            if (this.currentProjectId) this.downloadTractatusTrees(this.currentProjectId);
        });

        closeTractatusBtn?.addEventListener('click', () => {
            document.getElementById('tractatus-modal').style.display = 'none';
        });

        document.getElementById('tractatus-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'tractatus-modal') e.target.style.display = 'none';
        });
    }

    async loadMemoryProjects() {
        try {
            const res = await fetch(`/api/memory/projects?thinker=${this.selectedDatabase}`);
            const data = await res.json();
            this.memoryProjects = data.projects || [];
            const select = document.getElementById('memory-project-select');
            select.innerHTML = '<option value="">Select Project...</option>';
            this.memoryProjects.forEach(p => {
                const opt = document.createElement('option');
                opt.value = p.id;
                opt.textContent = p.name;
                select.appendChild(opt);
            });
            if (this.memoryProjects.length > 0 && !this.currentProjectId) {
                select.value = this.memoryProjects[0].id;
                this.currentProjectId = this.memoryProjects[0].id;
                await this.loadMemorySessions(this.currentProjectId);
            }
        } catch (e) {
            console.error('Error loading projects:', e);
        }
    }

    async createMemoryProject(name) {
        try {
            const res = await fetch('/api/memory/projects', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ name, thinker: this.selectedDatabase })
            });
            const data = await res.json();
            if (data.project) {
                await this.loadMemoryProjects();
                document.getElementById('memory-project-select').value = data.project.id;
                this.currentProjectId = data.project.id;
                await this.loadMemorySessions(data.project.id);
                return data.project;
            }
        } catch (e) {
            console.error('Error creating project:', e);
        }
        return null;
    }

    async deleteMemoryProject(projectId) {
        try {
            await fetch(`/api/memory/projects/${projectId}`, { method: 'DELETE' });
            this.currentProjectId = null;
            this.currentSessionId = null;
            await this.loadMemoryProjects();
            document.getElementById('memory-session-select').innerHTML = '<option value="">Select Session...</option>';
        } catch (e) {
            console.error('Error deleting project:', e);
        }
    }

    async loadMemorySessions(projectId) {
        try {
            const res = await fetch(`/api/memory/projects/${projectId}/sessions`);
            const data = await res.json();
            this.memorySessions = data.sessions || [];
            const select = document.getElementById('memory-session-select');
            select.innerHTML = '<option value="">Select Session...</option>';
            this.memorySessions.forEach(s => {
                const opt = document.createElement('option');
                opt.value = s.id;
                opt.textContent = s.title;
                select.appendChild(opt);
            });
            if (this.memorySessions.length === 0) {
                await this.createMemorySession(projectId, 'Session 1');
            } else if (this.memorySessions.length > 0) {
                select.value = this.memorySessions[0].id;
                this.currentSessionId = this.memorySessions[0].id;
            }
        } catch (e) {
            console.error('Error loading sessions:', e);
        }
    }

    async createMemorySession(projectId, title) {
        try {
            const res = await fetch(`/api/memory/projects/${projectId}/sessions`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ title })
            });
            const data = await res.json();
            if (data.session) {
                await this.loadMemorySessions(projectId);
                document.getElementById('memory-session-select').value = data.session.id;
                this.currentSessionId = data.session.id;
                this.messageContainer.innerHTML = '';
            }
        } catch (e) {
            console.error('Error creating session:', e);
        }
    }

    async renameMemorySession(sessionId, newTitle) {
        try {
            const res = await fetch(`/api/memory/sessions/${sessionId}`, {
                method: 'PATCH',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ title: newTitle })
            });
            if (res.ok && this.currentProjectId) {
                await this.loadMemorySessions(this.currentProjectId);
                document.getElementById('memory-session-select').value = sessionId;
                this.currentSessionId = sessionId;
            }
        } catch (e) {
            console.error('Error renaming session:', e);
        }
    }

    async deleteMemorySession(sessionId) {
        try {
            await fetch(`/api/memory/sessions/${sessionId}`, { method: 'DELETE' });
            this.currentSessionId = null;
            if (this.currentProjectId) {
                await this.loadMemorySessions(this.currentProjectId);
            }
            this.messageContainer.innerHTML = '';
        } catch (e) {
            console.error('Error deleting session:', e);
        }
    }

    async loadSessionTranscript(sessionId) {
        try {
            const res = await fetch(`/api/memory/sessions/${sessionId}/transcript`);
            const data = await res.json();
            const transcript = data.transcript || [];
            this.messageContainer.innerHTML = '';
            for (const msg of transcript) {
                if (msg.role === 'user') {
                    this.addUserMessage(msg.content);
                } else {
                    const div = this.addAssistantMessage(this.selectedDatabase, '', false);
                    const textDiv = div.querySelector('.message-text');
                    textDiv.textContent = msg.content;
                }
            }
            if (transcript.length > 0) {
                this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
            }
        } catch (e) {
            console.error('Error loading transcript:', e);
        }
    }

    async showTractatusTree(projectId) {
        try {
            const res = await fetch(`/api/memory/projects/${projectId}/memory-hierarchy`);
            const data = await res.json();
            this._lastTractatusData = data;
            const modal = document.getElementById('tractatus-modal');
            const content = document.getElementById('tractatus-tree-content');

            let html = '';
            const tree = data.current_tree || {};
            const keys = Object.keys(tree).sort((a, b) => {
                const pa = a.split('.').map(Number);
                const pb = b.split('.').map(Number);
                for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
                    if ((pa[i] || 0) !== (pb[i] || 0)) return (pa[i] || 0) - (pb[i] || 0);
                }
                return 0;
            });

            if (keys.length === 0) {
                html = '<p class="tractatus-empty">No memory yet. Start chatting in this project to build the memory tree.</p>';
            } else {
                html = '<div class="tractatus-nodes">';
                for (const key of keys) {
                    const value = tree[key];
                    const depth = key.split('.').length - 1;
                    const indent = depth * 20;
                    let tagClass = 'tag-default';
                    if (value.startsWith('ASSERTS:')) tagClass = 'tag-asserts';
                    else if (value.startsWith('REJECTS:')) tagClass = 'tag-rejects';
                    else if (value.startsWith('ASSUMES:')) tagClass = 'tag-assumes';
                    else if (value.startsWith('OPEN:')) tagClass = 'tag-open';
                    else if (value.startsWith('RESOLVED:')) tagClass = 'tag-resolved';
                    const safeValue = value.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                    const safeKey = key.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
                    html += `<div class="tractatus-node ${tagClass}" style="margin-left:${indent}px"><span class="node-key">${safeKey}</span> ${safeValue}</div>`;
                }
                html += '</div>';
            }

            if (data.archives && data.archives.length > 0) {
                html += '<h3 class="tractatus-archive-title">Archived Memory Tiers</h3>';
                for (const archive of data.archives) {
                    html += `<details class="tractatus-archive"><summary>Tier ${archive.tier} (${archive.node_count} nodes, ${new Date(archive.created_at).toLocaleDateString()})</summary>`;
                    html += `<pre class="tractatus-archive-content">${JSON.stringify(archive.tree, null, 2)}</pre></details>`;
                }
            }

            if (data.meta_trees && data.meta_trees.length > 0) {
                html += '<div class="meta-tractatus-section">';
                html += '<h3>🧬 Meta-Tractatus Trees</h3>';
                for (const meta of data.meta_trees) {
                    html += `<details class="tractatus-archive"><summary>Meta-Tree #${meta.id} (${meta.node_count} nodes, ${new Date(meta.created_at).toLocaleDateString()}) — spans archives ${meta.archive_start_id}–${meta.archive_end_id}</summary>`;
                    html += `<pre class="tractatus-archive-content">${JSON.stringify(meta.tree, null, 2)}</pre></details>`;
                }
                html += '</div>';
            }

            content.innerHTML = html;
            modal.style.display = 'flex';
        } catch (e) {
            console.error('Error loading tractatus:', e);
        }
    }

    async downloadTractatusTrees(projectId) {
        try {
            const data = this._lastTractatusData;
            if (!data) return;
            const projectName = document.getElementById('memory-project-select')
                ?.selectedOptions[0]?.textContent || 'project';
            const exportData = {
                project: projectName,
                exported_at: new Date().toISOString(),
                current_tree: data.current_tree || {},
                current_tier: data.current_tier || 1,
                archives: data.archives || [],
                meta_trees: data.meta_trees || []
            };
            const blob = new Blob([JSON.stringify(exportData, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `tractatus_${projectName.replace(/\s+/g, '_')}_${new Date().toISOString().slice(0,10)}.json`;
            a.click();
            URL.revokeObjectURL(url);
        } catch (e) {
            console.error('Error downloading tractatus:', e);
        }
    }
}

let workshop;
document.addEventListener('DOMContentLoaded', () => {
    workshop = new ThinkerWorkshop();
});

// === Longform Workshop ===
(function setupLongform() {
    const btn = document.getElementById('longform-btn');
    const modal = document.getElementById('longform-modal');
    const closeBtn = document.getElementById('close-longform-modal');
    const setupView = document.getElementById('lf-setup');
    const progressView = document.getElementById('lf-progress');
    const historyView = document.getElementById('lf-history');
    const startBtn = document.getElementById('lf-start-btn');
    const wordsSlider = document.getElementById('lf-target-words');
    const wordsValue = document.getElementById('lf-words-value');
    const promptInput = document.getElementById('lf-prompt');
    const thinkerSel = document.getElementById('lf-thinker');
    const modeSel = document.getElementById('lf-mode');
    const statusText = document.getElementById('lf-status-text');
    const wordCounter = document.getElementById('lf-word-counter');
    const progressFill = document.getElementById('lf-progress-fill');
    const skeletonView = document.getElementById('lf-skeleton-view');
    const sectionsView = document.getElementById('lf-sections');
    const downloadBtn = document.getElementById('lf-download-btn');
    const newBtn = document.getElementById('lf-new-btn');
    const historyBtn = document.getElementById('lf-history-btn');
    const historyBack = document.getElementById('lf-history-back');
    const historyList = document.getElementById('lf-history-list');

    if (!btn || !modal) return;

    let currentEventSource = null;
    let currentDocId = null;
    let currentSkeleton = null;
    let currentTitle = '';

    function showView(name) {
        setupView.style.display = name === 'setup' ? 'block' : 'none';
        progressView.style.display = name === 'progress' ? 'block' : 'none';
        historyView.style.display = name === 'history' ? 'block' : 'none';
    }

    function openModal() {
        modal.style.display = 'flex';
        showView('setup');
    }

    function closeModal() {
        modal.style.display = 'none';
        if (currentEventSource) {
            currentEventSource.close();
            currentEventSource = null;
        }
    }

    function escapeHtml(s) {
        return (s || '').replace(/[&<>"']/g, (c) => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[c]));
    }

    function paragraphsHtml(text) {
        return (text || '').split(/\n\s*\n/).filter(p => p.trim())
            .map(p => `<p>${escapeHtml(p.trim())}</p>`).join('');
    }

    function renderSkeleton(skel) {
        if (!skel) { skeletonView.innerHTML = ''; return; }
        const sectionsHtml = (skel.sections || []).map((s, i) => `
            <div class="lf-section-plan">
                <div class="lf-section-plan-title">§${i + 1}. ${escapeHtml(s.title)}
                    <span class="lf-section-plan-role">${escapeHtml(s.role || '')}</span>
                </div>
                <div style="font-size:0.83rem;color:#4B5563;">~${s.word_target || 0} words</div>
                ${s.claims_to_make && s.claims_to_make.length ? `<ul>${s.claims_to_make.map(c => `<li>${escapeHtml(c)}</li>`).join('')}</ul>` : ''}
            </div>
        `).join('');
        skeletonView.innerHTML = `
            <div class="lf-thesis"><strong>Thesis:</strong> ${escapeHtml(skel.thesis || '')}</div>
            <div style="margin-bottom:10px;font-size:0.85rem;color:#374151;"><strong>Arc:</strong> ${escapeHtml(skel.arc || '')}</div>
            ${skel.central_concepts && skel.central_concepts.length ? `<div style="margin-bottom:12px;font-size:0.85rem;color:#374151;"><strong>Central concepts:</strong> ${skel.central_concepts.map(escapeHtml).join(', ')}</div>` : ''}
            <div>${sectionsHtml}</div>
        `;
    }

    function ensureSectionCard(idx, title, role, wordTarget, pending) {
        let card = document.getElementById(`lf-section-${idx}`);
        if (!card) {
            card = document.createElement('div');
            card.id = `lf-section-${idx}`;
            card.className = 'lf-section-card' + (pending ? ' lf-section-pending' : '');
            sectionsView.appendChild(card);
        }
        return card;
    }

    function renderSectionStart(idx, total, title, role, wordTarget) {
        const card = ensureSectionCard(idx, title, role, wordTarget, true);
        card.innerHTML = `
            <div class="lf-section-card-header">
                <div class="lf-section-card-title">§${idx + 1}. ${escapeHtml(title)}</div>
                <div class="lf-section-card-meta">${escapeHtml(role || '')} • target ~${wordTarget} words • generating…</div>
            </div>
            <div class="lf-section-card-body">
                <em style="color:#6B7280;">Generating section ${idx + 1} of ${total}…</em>
            </div>
        `;
        card.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }

    function renderSectionComplete(idx, total, title, text, wordCount) {
        const card = ensureSectionCard(idx, title, '', 0, false);
        card.classList.remove('lf-section-pending');
        const headerMeta = card.querySelector('.lf-section-card-meta');
        const role = headerMeta ? (headerMeta.textContent.split('•')[0] || '').trim() : '';
        card.innerHTML = `
            <div class="lf-section-card-header">
                <div class="lf-section-card-title">§${idx + 1}. ${escapeHtml(title)}</div>
                <div class="lf-section-card-meta">${escapeHtml(role)} ${role ? '•' : ''} ${wordCount} words</div>
            </div>
            <div class="lf-section-card-body">${paragraphsHtml(text)}</div>
        `;
    }

    function updateProgress(cumulativeWords, target, completedSections, totalSections) {
        wordCounter.textContent = `${cumulativeWords.toLocaleString()} / ${target.toLocaleString()} words • ${completedSections}/${totalSections} sections`;
        const pct = Math.min(100, totalSections > 0 ? (completedSections / totalSections) * 100 : 0);
        progressFill.style.width = `${pct}%`;
    }

    function downloadDoc() {
        const cards = sectionsView.querySelectorAll('.lf-section-card:not(.lf-section-pending)');
        let out = `${currentTitle}\n${'='.repeat(currentTitle.length)}\n\n`;
        if (currentSkeleton && currentSkeleton.thesis) {
            out += `Thesis: ${currentSkeleton.thesis}\n\n`;
        }
        cards.forEach(card => {
            const title = card.querySelector('.lf-section-card-title')?.textContent || '';
            const body = Array.from(card.querySelectorAll('.lf-section-card-body p')).map(p => p.textContent).join('\n\n');
            out += `\n\n${title}\n${'-'.repeat(title.length)}\n\n${body}\n`;
        });
        const blob = new Blob([out], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `longform-${currentDocId || 'doc'}.txt`;
        a.click();
        URL.revokeObjectURL(url);
    }

    function streamDocument(docId, target) {
        currentDocId = docId;
        sectionsView.innerHTML = '';
        skeletonView.innerHTML = '';
        downloadBtn.style.display = 'none';
        showView('progress');
        statusText.textContent = 'Connecting…';
        wordCounter.textContent = `0 / ${target.toLocaleString()} words`;
        progressFill.style.width = '0%';

        if (currentEventSource) currentEventSource.close();
        const es = new EventSource(`/api/longform/coherent/${docId}/stream`);
        currentEventSource = es;

        let totalSections = 0;
        let completedSections = 0;
        let cumulativeWords = 0;

        es.addEventListener('snapshot', (ev) => {
            const data = JSON.parse(ev.data);
            currentSkeleton = data.skeleton;
            currentTitle = data.user_prompt;
            totalSections = data.total_sections || (data.skeleton?.sections?.length || 0);
            renderSkeleton(currentSkeleton);
            statusText.textContent = `Status: ${data.status}`;
            updateProgress(0, data.target_words, 0, totalSections);
        });

        es.addEventListener('status', (ev) => {
            const data = JSON.parse(ev.data);
            statusText.textContent = data.message || data.status;
        });

        es.addEventListener('skeleton', (ev) => {
            const data = JSON.parse(ev.data);
            currentSkeleton = data.skeleton;
            totalSections = currentSkeleton?.sections?.length || 0;
            renderSkeleton(currentSkeleton);
            updateProgress(cumulativeWords, target, completedSections, totalSections);
        });

        es.addEventListener('section_start', (ev) => {
            const data = JSON.parse(ev.data);
            statusText.textContent = `Generating §${data.index + 1}/${data.total} — ${data.title}`;
            renderSectionStart(data.index, data.total, data.title, data.role, data.wordTarget);
        });

        es.addEventListener('section_complete', (ev) => {
            const data = JSON.parse(ev.data);
            renderSectionComplete(data.index, data.total, data.title, data.text, data.wordCount);
            completedSections = Math.max(completedSections, data.index + 1);
            if (typeof data.cumulativeWords === 'number') {
                cumulativeWords = data.cumulativeWords;
            } else {
                cumulativeWords += (data.wordCount || 0);
            }
            updateProgress(cumulativeWords, target, completedSections, totalSections);
        });

        es.addEventListener('complete', (ev) => {
            statusText.textContent = `✓ Complete — ${cumulativeWords.toLocaleString()} words across ${completedSections} sections`;
            progressFill.style.width = '100%';
            downloadBtn.style.display = 'inline-block';
            es.close();
            currentEventSource = null;
        });

        es.addEventListener('error', (ev) => {
            try {
                const data = JSON.parse(ev.data);
                statusText.textContent = `✗ Error: ${data.message || 'unknown'}`;
            } catch {
                statusText.textContent = '✗ Connection lost. The job may still be running — close and re-open.';
            }
            es.close();
            currentEventSource = null;
        });
    }

    btn.addEventListener('click', openModal);
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

    wordsSlider.addEventListener('input', () => {
        wordsValue.textContent = parseInt(wordsSlider.value).toLocaleString();
    });

    startBtn.addEventListener('click', async () => {
        const prompt = promptInput.value.trim();
        if (!prompt) { alert('Please enter a prompt or topic.'); return; }
        const thinker = thinkerSel.value;
        const mode = modeSel.value;
        const targetWords = parseInt(wordsSlider.value);
        currentTitle = prompt.slice(0, 100);
        startBtn.disabled = true;
        startBtn.textContent = 'Starting…';
        try {
            const res = await fetch('/api/longform/coherent/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ thinker, prompt, mode, targetWords })
            });
            const data = await res.json();
            if (!data.success) throw new Error(data.error || 'Failed to start');
            streamDocument(data.documentId, targetWords);
        } catch (e) {
            alert('Failed to start: ' + e.message);
        } finally {
            startBtn.disabled = false;
            startBtn.textContent = 'Generate';
        }
    });

    newBtn.addEventListener('click', () => {
        if (currentEventSource) { currentEventSource.close(); currentEventSource = null; }
        showView('setup');
    });

    downloadBtn.addEventListener('click', downloadDoc);

    historyBtn.addEventListener('click', async () => {
        showView('history');
        historyList.innerHTML = '<em>Loading…</em>';
        try {
            const res = await fetch('/api/longform/coherent/list');
            const data = await res.json();
            const docs = data.documents || [];
            if (!docs.length) { historyList.innerHTML = '<em>No past jobs.</em>'; return; }
            historyList.innerHTML = docs.map(d => {
                const created = new Date(d.created_at).toLocaleString();
                const statusClass = `lf-status-${d.status}`;
                return `
                    <div class="lf-history-item" data-id="${d.document_id}" data-target="${d.target_words}">
                        <div class="lf-history-item-title">${escapeHtml((d.user_prompt || '').slice(0, 120))}${d.user_prompt && d.user_prompt.length > 120 ? '…' : ''}</div>
                        <div class="lf-history-item-meta">
                            <span class="lf-history-item-status ${statusClass}">${d.status}</span>
                            <span>${escapeHtml(d.thinker)} • ${escapeHtml(d.mode)}</span>
                            <span>${(d.total_words || 0).toLocaleString()} / ${(d.target_words || 0).toLocaleString()} words</span>
                            <span>§ ${d.current_section || 0}/${d.total_sections || 0}</span>
                            <span>${created}</span>
                            <button class="lf-history-delete" data-id="${d.document_id}">delete</button>
                        </div>
                    </div>
                `;
            }).join('');
            historyList.querySelectorAll('.lf-history-item').forEach(el => {
                el.addEventListener('click', (e) => {
                    if (e.target.classList.contains('lf-history-delete')) return;
                    const id = el.getAttribute('data-id');
                    const target = parseInt(el.getAttribute('data-target')) || 15000;
                    streamDocument(id, target);
                });
            });
            historyList.querySelectorAll('.lf-history-delete').forEach(b => {
                b.addEventListener('click', async (e) => {
                    e.stopPropagation();
                    const id = b.getAttribute('data-id');
                    if (!confirm('Delete this job?')) return;
                    await fetch(`/api/longform/coherent/${id}`, { method: 'DELETE' });
                    historyBtn.click();
                });
            });
        } catch (e) {
            historyList.innerHTML = `<em>Failed to load: ${e.message}</em>`;
        }
    });

    historyBack.addEventListener('click', () => showView('setup'));
})();

// ============== DIAGNOSTIC ==============
(function() {
    const btn = document.getElementById('diagnostic-btn');
    const modal = document.getElementById('diagnostic-modal');
    const closeBtn = document.getElementById('close-diagnostic-modal');
    const runBtn = document.getElementById('run-diagnostic-btn');
    const statusEl = document.getElementById('diagnostic-status');
    const summaryEl = document.getElementById('diagnostic-summary');
    const resultsEl = document.getElementById('diagnostic-results');
    if (!btn || !modal) return;

    btn.addEventListener('click', () => { modal.style.display = 'flex'; });
    closeBtn.addEventListener('click', () => { modal.style.display = 'none'; });
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.style.display = 'none'; });

    function renderResults(data) {
        const { summary, results } = data;
        const allPass = summary.failed === 0;
        summaryEl.style.display = 'flex';
        summaryEl.className = 'diagnostic-summary ' + (allPass ? 'all-pass' : 'has-fail');
        summaryEl.innerHTML = `
            <div class="stat"><strong>${summary.passed}</strong> / ${summary.total} passed</div>
            <div class="stat">${summary.failed > 0 ? '<strong>' + summary.failed + '</strong> failed' : 'All systems nominal'}</div>
            <div class="stat" style="margin-left:auto;color:#64748B;font-size:12px;">${summary.timestamp}</div>
        `;

        // Group by category preserving order
        const grouped = {};
        const order = [];
        for (const r of results) {
            if (!grouped[r.category]) { grouped[r.category] = []; order.push(r.category); }
            grouped[r.category].push(r);
        }
        const html = order.map(cat => {
            const rows = grouped[cat].map(r => `
                <div class="diagnostic-row ${r.status}">
                    <div class="diag-icon">${r.status === 'pass' ? '✅' : '❌'}</div>
                    <div>
                        <div class="diag-name">${r.name}</div>
                        <div class="diag-detail">${r.detail}</div>
                    </div>
                    <div class="diag-status ${r.status}">${r.status.toUpperCase()}</div>
                    <div class="diag-ms">${r.ms} ms</div>
                </div>
            `).join('');
            return `<div class="diagnostic-category-header">${cat}</div>${rows}`;
        }).join('');
        resultsEl.innerHTML = html;
    }

    runBtn.addEventListener('click', async () => {
        runBtn.disabled = true;
        statusEl.textContent = 'Running checks (this may take ~10-20 seconds)...';
        resultsEl.innerHTML = '';
        summaryEl.style.display = 'none';
        try {
            const resp = await fetch('/api/diagnostic/run', { method: 'POST' });
            if (!resp.ok) throw new Error('HTTP ' + resp.status);
            const data = await resp.json();
            renderResults(data);
            statusEl.textContent = '';
        } catch (e) {
            statusEl.textContent = 'Diagnostic request failed: ' + e.message;
        } finally {
            runBtn.disabled = false;
        }
    });
})();
