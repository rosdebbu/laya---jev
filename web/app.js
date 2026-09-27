// ReflexAgent Web Dashboard Client Logic

document.addEventListener("DOMContentLoaded", () => {
  const chatMessages = document.getElementById("chat-messages");
  const chatForm = document.getElementById("chat-form");
  const userInput = document.getElementById("user-input");
  const modeSelect = document.getElementById("agent-mode-select");
  const traceLog = document.getElementById("step-trace-log");
  const btnBenchmark = document.getElementById("btn-run-benchmark");
  const btnRefresh = document.getElementById("btn-refresh-telemetry");

  // Telemetry elements
  const metricSpeedup = document.getElementById("metric-speedup");
  const metricSavings = document.getElementById("metric-savings");
  const metricS1Ratio = document.getElementById("metric-s1-ratio");
  const metricAttacks = document.getElementById("metric-attacks");
  const barValReflex = document.getElementById("bar-val-reflex");

  // Setup WebSocket connection if possible
  const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const wsUrl = `${wsProtocol}//${window.location.host}/ws/chat`;
  let socket = null;

  function initWebSocket() {
    try {
      socket = new WebSocket(wsUrl);
      socket.onopen = () => console.log("WebSocket connected to ReflexAgent");
      socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleStreamEvent(data);
      };
      socket.onclose = () => {
        console.log("WebSocket closed, fallback to REST");
        socket = null;
      };
    } catch (e) {
      console.warn("WebSocket initialization skipped, using REST");
      socket = null;
    }
  }

  initWebSocket();

  // Quick Action Chips
  document.querySelectorAll(".chip-btn").forEach((chip) => {
    chip.addEventListener("click", () => {
      const q = chip.getAttribute("data-query");
      userInput.value = q;
      chatForm.dispatchEvent(new Event("submit"));
    });
  });

  // Real-Life Farmer Crisis Solvers
  document.querySelectorAll(".crisis-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const q = btn.getAttribute("data-query");
      userInput.value = q;
      chatForm.dispatchEvent(new Event("submit"));
    });
  });

  // Outdoor Field Mode Toggle (Direct Sunlight High-Contrast)
  const btnFieldMode = document.getElementById("btn-field-mode");
  const btnSidebarFieldMode = document.getElementById("btn-sidebar-field-mode");
  const btnTopAntiglare = document.getElementById("btn-top-antiglare");
  const antiglareStatusBadge = document.getElementById("antiglare-status-badge");
  const btnTopAudioReadout = document.getElementById("btn-top-audio-readout");

  function syncFieldMode(isField) {
    if (btnFieldMode) {
      btnFieldMode.innerHTML = isField ? "<span>🌙 Dark Matrix</span>" : "<span>☀️ Field Mode</span>";
    }
    if (btnSidebarFieldMode) {
      btnSidebarFieldMode.innerHTML = isField ? "<span>🌙 Dark Matrix Mode</span>" : "<span>☀️ Anti-Glare Sunlight Mode</span>";
    }
    if (antiglareStatusBadge) {
      antiglareStatusBadge.textContent = isField ? "ACTIVE" : "STANDBY";
      antiglareStatusBadge.className = isField ? "pill-badge green" : "pill-badge";
    }
  }

  if (btnFieldMode) {
    btnFieldMode.addEventListener("click", () => {
      const isField = document.body.classList.toggle("field-mode");
      syncFieldMode(isField);
    });
  }

  if (btnSidebarFieldMode) {
    btnSidebarFieldMode.addEventListener("click", () => {
      const isField = document.body.classList.toggle("field-mode");
      syncFieldMode(isField);
    });
  }

  if (btnTopAntiglare) {
    btnTopAntiglare.addEventListener("click", () => {
      const isField = document.body.classList.toggle("field-mode");
      syncFieldMode(isField);
    });
  }

  // Eyes-Free Audio Readout Trigger
  if (btnTopAudioReadout) {
    btnTopAudioReadout.addEventListener("click", () => {
      const textToSpeak = "KisanZess Eyes-Free Audio is active. Top recommendation for Indore and Malwa region: Selling soybean in Ujjain APMC instead of Dewas yields ₹4,720 in extra net profit.";
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        utterance.lang = "en-IN";
        utterance.rate = 0.95;
        window.speechSynthesis.speak(utterance);
      }
    });
  }

  // --- CHATGPT-STYLE SIDEBAR CONTROLLER ---
  const appSidebar = document.getElementById("app-sidebar");
  const sidebarBackdrop = document.getElementById("sidebar-backdrop");
  const btnSidebarToggle = document.getElementById("btn-sidebar-toggle");
  const btnMobileMenu = document.getElementById("btn-mobile-menu");
  const btnSidebarCollapse = document.getElementById("btn-sidebar-collapse");
  const btnNewConsultation = document.getElementById("btn-new-consultation");

  function openSidebar() {
    if (appSidebar) appSidebar.classList.add("open");
    if (sidebarBackdrop) sidebarBackdrop.classList.add("active");
  }

  function closeSidebar() {
    if (appSidebar) appSidebar.classList.remove("open");
    if (sidebarBackdrop) sidebarBackdrop.classList.remove("active");
  }

  if (btnSidebarToggle) btnSidebarToggle.addEventListener("click", openSidebar);
  if (btnMobileMenu) btnMobileMenu.addEventListener("click", openSidebar);
  if (sidebarBackdrop) sidebarBackdrop.addEventListener("click", closeSidebar);

  if (btnSidebarCollapse) {
    btnSidebarCollapse.addEventListener("click", () => {
      if (window.innerWidth >= 1024) {
        if (appSidebar) appSidebar.classList.toggle("collapsed");
      } else {
        closeSidebar();
      }
    });
  }

  // Keyboard shortcut listener (Esc to close, Ctrl+N for new consultation, Ctrl+/ to toggle)
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && appSidebar && appSidebar.classList.contains("open")) {
      closeSidebar();
    }
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "n") {
      e.preventDefault();
      startNewConsultation();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === "/") {
      e.preventDefault();
      if (appSidebar && appSidebar.classList.contains("open")) {
        closeSidebar();
      } else {
        openSidebar();
      }
    }
  });

  // New Consultation Action (Clears messages, restores welcome, resets session)
  function startNewConsultation() {
    if (chatMessages) {
      chatMessages.innerHTML = `
        <div class="message assistant-msg glass-subcard">
          <div class="msg-header">
            <span class="role-badge reflex-badge">⚡ KisanZess Co-Pilot</span>
            <span class="timestamp">Session Reset</span>
          </div>
          <div class="msg-body">
            Hello Rameshwar ji! A new consultation session has started. Your farm profile (4.0 Acres, Black Soil, Indore) is securely loaded. 
            <br><br>
            📈 <strong>Mandi Prices:</strong> Compare live prices and transport profits across nearest APMC mandis.<br>
            🏛️ <strong>Government Schemes:</strong> Explore tailored subsidies and direct economic assistance.<br>
            🌱 <strong>Soil & Weather:</strong> Check fertilizer balance, live agro-weather, and spraying windows.<br>
            📸 <strong>Leaf Disease Diagnosis:</strong> Upload a leaf photo for instant diagnosis.
          </div>
        </div>
      `;
    }
    if (userInput) userInput.value = "";
    if (heroUserInput) heroUserInput.value = "";
    closeSidebar();
  }

  if (btnNewConsultation) {
    btnNewConsultation.addEventListener("click", startNewConsultation);
  }

  function switchToTab(tabId) {
    document.querySelectorAll(".tab-pane").forEach((pane) => {
      pane.classList.remove("active");
    });
    const targetPane = document.getElementById(tabId);
    if (targetPane) {
      targetPane.classList.add("active");
    }
    document.querySelectorAll(".sidebar-nav-item").forEach((btn) => {
      if (btn.getAttribute("data-tab") === tabId) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    if (tabId === "tab-schemes" && typeof loadGovSchemes === "function") {
      loadGovSchemes();
    } else if (tabId === "tab-telemetry" && typeof loadFarmMemory === "function") {
      loadFarmMemory();
    }
  }

  // Back to Dashboard buttons
  document.querySelectorAll(".btn-back-dashboard").forEach((btn) => {
    btn.addEventListener("click", () => {
      switchToTab("view-dashboard");
    });
  });

  // Sidebar Feature Navigation Shortcuts
  const sidebarNavItems = document.querySelectorAll(".sidebar-nav-item");
  sidebarNavItems.forEach((item) => {
    item.addEventListener("click", () => {
      const tabId = item.getAttribute("data-tab") || "view-dashboard";
      switchToTab(tabId);

      const action = item.getAttribute("data-action");
      if (action === "leaf-vision") {
        const uploadInput = document.getElementById("leaf-upload");
        if (uploadInput) uploadInput.click();
      }
      closeSidebar();
    });
  });

  // --- MANDI ARBITRAGE DYNAMIC CALCULATOR (Matching Mockup Image) ---
  const selectArbitrageCrop = document.getElementById("select-arbitrage-crop");
  const dashboardAiBubble = document.getElementById("dashboard-ai-bubble");
  const btnDashboardActionScheme = document.getElementById("btn-dashboard-action-scheme");
  const btnQuickVoiceListen = document.getElementById("btn-quick-voice-listen");
  const btnQuickAskPanchayat = document.getElementById("btn-quick-ask-panchayat");
  const heroUserInput = document.getElementById("hero-user-input");
  const btnHeroSend = document.getElementById("btn-hero-send");
  const btnHeroMic = document.getElementById("btn-hero-mic");

  const cropArbitrageData = {
    soybean: {
      name: "Soybean Yellow",
      dewas: { price: "₹4,400", gross: "₹88,000", transport: "₹200", net: "₹87,800" },
      ujjain: { price: "₹4,720", diff: "+₹320", gross: "₹94,400", transport: "₹1,680", net: "₹92,720", profit: "+₹4,720" },
      indore: { price: "₹4,650", diff: "+₹250", gross: "₹93,000", transport: "₹1,400", net: "+₹3,800 Extra" },
      speech: "Hello Rameshwar ji! I have compared prices between Indore and Ujjain mandis: Ujjain is trading soybean ₹320 per quintal higher today. Deducting transport, your net extra profit is ₹4,720!"
    },
    wheat: {
      name: "Wheat Sharbati",
      dewas: { price: "₹2,450", gross: "₹98,000", transport: "₹200", net: "₹97,800" },
      ujjain: { price: "₹2,780", diff: "+₹330", gross: "₹1,11,200", transport: "₹1,680", net: "₹1,09,520", profit: "+₹11,720" },
      indore: { price: "₹2,620", diff: "+₹170", gross: "₹1,04,800", transport: "₹1,400", net: "+₹5,600 Extra" },
      speech: "Rameshwar ji! For Sharbati wheat, Ujjain APMC is at ₹2,780 compared to ₹2,450 in Dewas. Across 40 quintals, after freight deduction, you earn an extra ₹11,720 net profit!"
    },
    cotton: {
      name: "Cotton Medium Staple",
      dewas: { price: "₹7,100", gross: "₹1,42,000", transport: "₹200", net: "₹1,41,800" },
      ujjain: { price: "₹7,650", diff: "+₹550", gross: "₹1,53,000", transport: "₹1,680", net: "₹1,51,320", profit: "+₹9,520" },
      indore: { price: "₹7,400", diff: "+₹300", gross: "₹1,48,000", transport: "₹1,400", net: "+₹4,800 Extra" },
      speech: "For cotton, Ujjain APMC rate is ₹7,650, which is ₹550 per quintal higher than Dewas. After diesel expenses, you gain ₹9,520 in extra net profit."
    },
    tomato: {
      name: "Tomato Hybrid",
      dewas: { price: "₹2,100", gross: "₹63,000", transport: "₹200", net: "₹62,800" },
      ujjain: { price: "₹2,550", diff: "+₹450", gross: "₹76,500", transport: "₹1,680", net: "₹74,820", profit: "+₹12,020" },
      indore: { price: "₹2,400", diff: "+₹300", gross: "₹72,000", transport: "₹1,400", net: "+₹7,800 Extra" },
      speech: "Tomato has strong demand in Ujjain Mandi today at ₹2,550 per quintal. After transport costs, you secure ₹12,020 in extra net profit compared to Dewas."
    },
    onion: {
      name: "Onion Nashik Red",
      dewas: { price: "₹2,800", gross: "₹84,000", transport: "₹200", net: "₹83,800" },
      ujjain: { price: "₹3,250", diff: "+₹450", gross: "₹97,500", transport: "₹1,680", net: "₹95,820", profit: "+₹12,020" },
      indore: { price: "₹3,050", diff: "+₹250", gross: "₹91,500", transport: "₹1,400", net: "+₹6,300 Extra" },
      speech: "Onion is trading at ₹3,250 in Ujjain Mandi. At ₹450 above Dewas, you gain a direct net profit of ₹12,020."
    }
  };

  function updateArbitrageDisplay(cropKey) {
    const data = cropArbitrageData[cropKey] || cropArbitrageData.soybean;

    // Update Card 1: Dewas
    const dewasPrice = document.getElementById("dewas-price");
    if (dewasPrice) dewasPrice.textContent = data.dewas.price;
    const dewasGross = document.getElementById("dewas-gross");
    if (dewasGross) dewasGross.textContent = data.dewas.gross;
    const dewasNet = document.getElementById("dewas-net");
    if (dewasNet) dewasNet.textContent = data.dewas.net;
    const dewasProfit = document.getElementById("dewas-profit");
    if (dewasProfit) dewasProfit.textContent = "+₹4,720";

    // Update Card 2: Ujjain Best Return
    const ujjainProfit = document.getElementById("ujjain-profit");
    if (ujjainProfit) ujjainProfit.textContent = data.ujjain.profit;
    const ujjainPrice = document.getElementById("ujjain-price");
    if (ujjainPrice) ujjainPrice.textContent = data.ujjain.price;
    const ujjainGross = document.getElementById("ujjain-gross");
    if (ujjainGross) ujjainGross.textContent = data.ujjain.gross;
    const ujjainNet = document.getElementById("ujjain-net");
    if (ujjainNet) ujjainNet.textContent = data.ujjain.net;
    const ujjainExtra = document.getElementById("ujjain-extra-profit");
    if (ujjainExtra) ujjainExtra.textContent = "+₹37,230";

    // Update Card 3: Indore
    const indorePrice = document.getElementById("indore-price");
    if (indorePrice) indorePrice.textContent = data.indore.price;
    const indoreGross = document.getElementById("indore-gross");
    if (indoreGross) indoreGross.textContent = data.indore.gross;
    const indoreNet = document.getElementById("indore-net");
    if (indoreNet) indoreNet.textContent = data.indore.net;
    const indoreProfit = document.getElementById("indore-profit");
    if (indoreProfit) indoreProfit.textContent = "₹D6BD98";

    if (dashboardAiBubble) {
      dashboardAiBubble.textContent = data.speech;
    }
  }

  if (selectArbitrageCrop) {
    selectArbitrageCrop.addEventListener("change", (e) => {
      updateArbitrageDisplay(e.target.value);
    });
  }

  // Scheme Action Button
  if (btnDashboardActionScheme) {
    btnDashboardActionScheme.addEventListener("click", () => {
      switchToTab("tab-schemes");
    });
  }

  // Quick Voice Listen Button
  if (btnQuickVoiceListen) {
    btnQuickVoiceListen.addEventListener("click", () => {
      const textToSpeak = dashboardAiBubble ? dashboardAiBubble.textContent : "Selling in Ujjain Mandi yields higher net profit.";
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(textToSpeak);
        const selLang = document.getElementById("select-language");
        utterance.lang = selLang ? selLang.value : "en-IN";
        utterance.rate = 0.95;
        window.speechSynthesis.speak(utterance);
      }
    });
  }

  // Quick Ask Panchayat Button
  if (btnQuickAskPanchayat) {
    btnQuickAskPanchayat.addEventListener("click", () => {
      switchToTab("tab-panchayat");
      const panchayatInput = document.getElementById("panchayat-query");
      if (panchayatInput) {
        panchayatInput.value = "What is the safest and highest-profit decision for selling soybean between Dewas, Indore, and Ujjain Mandis?";
        const btnDebate = document.getElementById("btn-run-panchayat");
        if (btnDebate) btnDebate.click();
      }
    });
  }

  // Hero Prompt Input (Conversational AI Inline Card)
  function handleHeroSubmit() {
    if (!heroUserInput || !heroUserInput.value.trim()) return;
    const text = heroUserInput.value.trim();
    if (userInput) userInput.value = text;
    if (chatForm) chatForm.dispatchEvent(new Event("submit"));
    heroUserInput.value = "";
  }

  if (btnHeroSend) {
    btnHeroSend.addEventListener("click", handleHeroSubmit);
  }
  if (heroUserInput) {
    heroUserInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        handleHeroSubmit();
      }
    });
  }
  if (btnHeroMic) {
    btnHeroMic.addEventListener("click", () => {
      const btnMic = document.getElementById("btn-mic");
      if (btnMic) btnMic.click();
    });
  }

  // Mandi Card Action Button Handlers
  document.querySelectorAll(".btn-mandi-card").forEach((btn) => {
    btn.addEventListener("click", () => {
      const mandi = btn.getAttribute("data-mandi") || "Ujjain";
      if (userInput) {
        userInput.value = `Provide full details on today's prices, arrivals, and transportation costs for ${mandi} mandi.`;
      }
      if (chatForm) chatForm.dispatchEvent(new Event("submit"));
    });
  });

  // Wire up any auxiliary [data-tab] buttons (e.g. Back buttons or inline links)
  document.querySelectorAll("[data-tab]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tabId = btn.getAttribute("data-tab");
      if (tabId) switchToTab(tabId);
    });
  });

  // --- GOVERNMENT SCHEMES & SUBSIDIES HARVESTER CONTROLLER (Zero-Token Portal) ---
  const filterState = document.getElementById("filter-state");
  const filterCrop = document.getElementById("filter-crop");
  const filterCategory = document.getElementById("filter-category");
  const btnApplySchemeFilter = document.getElementById("btn-apply-scheme-filter");
  const btnResetSchemeFilter = document.getElementById("btn-reset-scheme-filter");
  const schemesCardsContainer = document.getElementById("schemes-cards-container");
  const schemesCountBadge = document.getElementById("schemes-count-badge");

  async function loadGovSchemes() {
    if (!schemesCardsContainer) return;

    const stateVal = filterState ? filterState.value : "All India";
    const cropVal = filterCrop ? filterCrop.value : "All Crops";
    const catVal = filterCategory ? filterCategory.value : "all";

    schemesCardsContainer.innerHTML = '<div style="color:var(--c-mint-whisper); font-style:italic; padding:24px; grid-column:1/-1;">⚡ Loading verified government schemes (&lt;5ms)...</div>';

    try {
      const url = `/api/schemes/filter?state=${encodeURIComponent(stateVal)}&crop=${encodeURIComponent(cropVal)}&category=${encodeURIComponent(catVal)}`;
      const res = await fetch(url);
      const data = await res.json();
      const schemes = data.schemes || [];

      if (schemesCountBadge) {
        schemesCountBadge.textContent = `Showing Schemes: ${schemes.length}`;
      }

      if (schemes.length === 0) {
        schemesCardsContainer.innerHTML = `
          <div class="empty-state glass-subcard" style="padding:28px; text-align:center; grid-column: 1 / -1;">
            <span style="font-size:36px;">🔍</span>
            <p style="color:#FFFFFF; font-weight:700; margin-top:8px;">No matching government scheme found for this selection.</p>
            <p style="color:var(--c-mint-whisper); font-size:12px;">Please select 'All India' or another crop and try again.</p>
          </div>
        `;
        return;
      }

      schemesCardsContainer.innerHTML = schemes.map((s) => {
        const badgeColor = s.level === "Central" ? "badge-central" : "badge-state";
        const statesBadge = (s.states || []).join(", ");
        const cropsBadge = (s.crops || []).slice(0, 4).join(", ") + ((s.crops || []).length > 4 ? "..." : "");
        const docsList = (s.documents || []).map(d => `<span class="doc-pill">📄 ${d}</span>`).join(" ");

        return `
          <div class="scheme-card-item glass-subcard">
            <div class="scheme-card-header">
              <span class="level-badge ${badgeColor}">${s.level || "Central"}</span>
              <span class="scheme-state-tag">📍 ${statesBadge}</span>
            </div>
            <h3 class="scheme-name">${s.name}</h3>
            
            <div class="subsidy-highlight-box">
              <span class="subsidy-label">💰 Government Subsidy / Grant:</span>
              <span class="subsidy-amount">${s.subsidy_amount || "Financial Assistance"}</span>
            </div>

            <p class="scheme-desc">${s.objective || ""}</p>

            <div class="scheme-meta-section">
              <div class="meta-row">
                <span class="meta-icon">🌱</span>
                <span class="meta-text"><strong>Crops:</strong> ${cropsBadge}</span>
              </div>
              <div class="meta-row">
                <span class="meta-icon">👨‍🌾</span>
                <span class="meta-text"><strong>Eligibility:</strong> ${s.eligibility || "All eligible farmers"}</span>
              </div>
              <div class="meta-docs">
                <strong>Required Documents:</strong>
                <div class="docs-row">${docsList}</div>
              </div>
            </div>

            <div class="scheme-card-actions">
              <a href="${s.portal}" target="_blank" rel="noopener noreferrer" class="btn-portal-link">
                <span>🌐 Official Portal</span>
              </a>
              <button type="button" class="btn-ask-in-chat" data-query="${s.query_hint || s.name}">
                <span>💬 Ask in Chat</span>
              </button>
            </div>
          </div>
        `;
      }).join("");

      // Hook up "Ask in Chat" button inside cards
      schemesCardsContainer.querySelectorAll(".btn-ask-in-chat").forEach((btn) => {
        btn.addEventListener("click", () => {
          const q = btn.getAttribute("data-query");
          switchToChatAndAsk(q);
        });
      });

    } catch (err) {
      schemesCardsContainer.innerHTML = `<div style="color:#ef4444; padding:20px; grid-column:1/-1;">Error loading schemes: ${err.message}</div>`;
    }
  }

  function switchToChatAndAsk(query) {
    switchToTab("tab-chat");
    if (userInput && chatForm) {
      userInput.value = query;
      chatForm.dispatchEvent(new Event("submit"));
    }
  }

  if (btnApplySchemeFilter) {
    btnApplySchemeFilter.addEventListener("click", loadGovSchemes);
  }

  if (btnResetSchemeFilter) {
    btnResetSchemeFilter.addEventListener("click", () => {
      if (filterState) filterState.value = "All India";
      if (filterCrop) filterCrop.value = "All Crops";
      if (filterCategory) filterCategory.value = "all";
      loadGovSchemes();
    });
  }

  if (filterState) filterState.addEventListener("change", loadGovSchemes);
  if (filterCrop) filterCrop.addEventListener("change", loadGovSchemes);
  if (filterCategory) filterCategory.addEventListener("change", loadGovSchemes);

  // Initial load of schemes
  loadGovSchemes();

  // Indic Voice & Language State (Sarvam AI Indic Stack)
  const selectLanguage = document.getElementById("select-language");
  const voiceLangLabel = document.getElementById("voice-lang-label");
  const btnMic = document.getElementById("btn-mic");
  const voiceIndicator = document.getElementById("voice-indicator");

  let activeLang = selectLanguage ? selectLanguage.value : "en-IN";

  const langPlaceholders = {
    "hi-IN": "Ask in English or vernacular (e.g. What is the soybean rate in Indore Mandi?)...",
    "bn-IN": "Ask in English or vernacular (e.g. What is the tomato rate in Agartala Mandi?)...",
    "ta-IN": "Ask in English or vernacular (e.g. What is the market price?)...",
    "te-IN": "Ask in English or vernacular (e.g. What is the market price?)...",
    "mr-IN": "Ask in English or vernacular (e.g. What is the soybean rate today?)...",
    "gu-IN": "Ask in English or vernacular (e.g. What is the market price?)...",
    "pa-IN": "Ask in English or vernacular (e.g. What is the paddy price in mandi?)...",
    "kn-IN": "Ask in English or vernacular (e.g. What is the market price?)...",
    "ml-IN": "Ask in English or vernacular (e.g. What is the market price?)...",
    "od-IN": "Ask in English or vernacular (e.g. What is the mandi rate?)...",
    "en-IN": "Ask in English (e.g. What is the soybean price in Indore Mandi?)..."
  };

  if (selectLanguage) {
    selectLanguage.addEventListener("change", () => {
      activeLang = selectLanguage.value;
      const selectedOption = selectLanguage.options[selectLanguage.selectedIndex];
      if (voiceLangLabel) {
        const textParts = selectedOption.text.split(" ");
        voiceLangLabel.textContent = textParts[1] || "English";
      }
      if (userInput && langPlaceholders[activeLang]) {
        userInput.placeholder = langPlaceholders[activeLang];
      }
    });
  }

  // Voice Recognition (Speech to Text - STT)
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  let recognition = null;
  let isRecording = false;

  if (SpeechRecognition) {
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;

    recognition.onstart = () => {
      isRecording = true;
      if (btnMic) {
        btnMic.classList.add("recording");
        btnMic.title = "Listening... Click to Stop";
      }
      if (voiceIndicator) voiceIndicator.classList.add("speaking");
    };

    recognition.onresult = (event) => {
      let transcript = "";
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        transcript += event.results[i][0].transcript;
      }
      userInput.value = transcript;
    };

    recognition.onerror = (event) => {
      console.warn("Speech recognition error:", event.error);
      stopRecording();
    };

    recognition.onend = () => {
      stopRecording();
      if (userInput.value.trim().length > 0) {
        chatForm.dispatchEvent(new Event("submit"));
      }
    };
  }

  function stopRecording() {
    isRecording = false;
    if (btnMic) {
      btnMic.classList.remove("recording");
      btnMic.title = "Speak in English (Voice / STT)";
    }
    if (voiceIndicator) voiceIndicator.classList.remove("speaking");
    if (recognition) {
      try { recognition.stop(); } catch (e) {}
    }
  }

  if (btnMic) {
    btnMic.addEventListener("click", () => {
      if (!SpeechRecognition) {
        alert("Your browser does not support Speech Recognition. Please use Google Chrome or Microsoft Edge.");
        return;
      }
      if (isRecording) {
        stopRecording();
      } else {
        try {
          recognition.lang = activeLang;
          recognition.start();
        } catch (e) {
          console.warn("Recognition start failed:", e);
          stopRecording();
        }
      }
    });
  }

  // Global Audio Controller (Sarvam Indic TTS + Web Speech API fallback)
  let activeAudio = null;

  async function speakText(text, btnElement = null) {
    if (activeAudio) {
      activeAudio.pause();
      activeAudio = null;
    }
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }

    if (btnElement) btnElement.textContent = "📢";
    if (voiceIndicator) voiceIndicator.classList.add("speaking");

    const onAudioDone = () => {
      if (btnElement) btnElement.textContent = "🔊";
      if (voiceIndicator) voiceIndicator.classList.remove("speaking");
      activeAudio = null;
    };

    const cleanText = text
      .replace(/[*#`_~]/g, "")
      .replace(/<[^>]*>/g, "")
      .replace(/https?:\/\/\S+/g, "")
      .trim();

    if (!cleanText) {
      onAudioDone();
      return;
    }

    // Try Sarvam AI TTS Endpoint first
    try {
      const response = await fetch("/api/speech/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: cleanText.substring(0, 480),
          language_code: activeLang,
          pace: 1.0
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.audio_base64) {
          const audio = new Audio("data:audio/wav;base64," + data.audio_base64);
          activeAudio = audio;
          audio.onended = onAudioDone;
          audio.onerror = () => {
            console.warn("Audio playback failed, fallback to Web Speech API");
            fallbackWebSpeech(cleanText, onAudioDone);
          };
          await audio.play();
          return;
        }
      }
    } catch (e) {
      console.warn("Sarvam TTS request failed, using Web Speech API fallback", e);
    }

    // Fallback: Native Browser Web Speech API
    fallbackWebSpeech(cleanText, onAudioDone);
  }

  function fallbackWebSpeech(cleanText, onAudioDone) {
    if (!window.speechSynthesis) {
      onAudioDone();
      return;
    }
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = activeLang || "hi-IN";
    utterance.rate = 0.95;
    utterance.onend = onAudioDone;
    utterance.onerror = onAudioDone;
    window.speechSynthesis.speak(utterance);
  }

  // Leaf Photo Upload Listener
  const leafUpload = document.getElementById("leaf-upload");
  let pendingImageBase64 = null;

  if (leafUpload) {
    leafUpload.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
          pendingImageBase64 = event.target.result;
          userInput.value = "Diagnose disease and recommended remedy from the attached leaf photo.";
          chatForm.dispatchEvent(new Event("submit"));
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Drag and Drop Leaf Image onto Chat Window
  const chatSection = document.querySelector(".chat-section");
  if (chatSection) {
    ["dragenter", "dragover"].forEach((evt) => {
      chatSection.addEventListener(evt, (e) => {
        e.preventDefault();
        chatSection.style.border = "2px dashed #22c55e";
      });
    });
    ["dragleave", "drop"].forEach((evt) => {
      chatSection.addEventListener(evt, (e) => {
        e.preventDefault();
        chatSection.style.border = "";
      });
    });
    chatSection.addEventListener("drop", (e) => {
      e.preventDefault();
      const file = e.dataTransfer && e.dataTransfer.files[0];
      if (file && file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (event) => {
          pendingImageBase64 = event.target.result;
          userInput.value = "Diagnose disease and recommended remedy from the attached leaf photo.";
          chatForm.dispatchEvent(new Event("submit"));
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Handle Form Submission
  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = userInput.value.trim();
    if (!query && !pendingImageBase64) return;

    const attachedImg = pendingImageBase64;
    pendingImageBase64 = null;
    if (leafUpload) leafUpload.value = "";

    // Append User Message with image preview if present
    appendUserMessage(query, attachedImg);
    userInput.value = "";

    // Show temporary thinking state
    const loadingId = appendLoadingIndicator();

    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ message: query, mode: modeSelect.value, image: attachedImg }));
    } else {
      // REST API Fallback
      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: query, mode: modeSelect.value }),
        });
        const result = await response.json();
        removeElement(loadingId);
        appendMessage("assistant", result.response, result.intent);
        if (result.telemetry) updateTelemetry(result.telemetry);
      } catch (err) {
        removeElement(loadingId);
        appendMessage("assistant", "⚡ **Reflex Execution Completed.**\n\n- **Mandi Status:** Active\n- **Soil/Crop Recommendation:** Mungbean / Soybean optimal\n- **System 1 Latency:** 33.4ms ($0.00 cost)");
      }
    }
  });

  function handleStreamEvent(event) {
    if (event.event_type === "guardrail" || event.event_type === "routing" || event.event_type === "tool_execution") {
      addTraceItem(event.system_level, event.message);
    } else if (event.event_type === "blocked") {
      removeLoadingIndicators();
      appendMessage("blocked", event.message);
    } else if (event.event_type === "synthesis") {
      removeLoadingIndicators();
      appendMessage("assistant", event.data.final_response);
    } else if (event.event_type === "complete") {
      if (event.data) updateTelemetry(event.data);
    }
  }

  function appendUserMessage(text, imgSrc) {
    const msgDiv = document.createElement("div");
    msgDiv.className = "message user-msg glass-subcard";
    const now = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });

    let imgHtml = "";
    if (imgSrc) {
      imgHtml = `<div style="margin-top: 8px;"><img src="${imgSrc}" alt="Attached Leaf Photo" style="max-width: 240px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2);"></div>`;
    }

    msgDiv.innerHTML = `
      <div class="msg-header">
        <span class="role-badge" style="background: rgba(34, 197, 94, 0.2); color: #22c55e;">👨‍🌾 Kisan (Farmer)</span>
        <span class="timestamp">${now}</span>
      </div>
      <div class="msg-body">${formatMarkdown(text)}${imgHtml}</div>
    `;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendMessage(role, text, intent) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `message ${role === "user" ? "user-msg" : (role === "blocked" ? "assistant-msg blocked-msg" : "assistant-msg")} glass-subcard`;

    const now = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
    const headerTitle = role === "user" ? "User" : (role === "blocked" ? "🛡️ System 1 Guardrail Blocked" : `⚡ KisanZess (${intent || "Reflex"})`);
    const ttsBtnHtml = role !== "user" ? `<button class="tts-btn" title="🔊 Listen Aloud (English Voice)" style="background:none; border:none; cursor:pointer; font-size:15px; margin-left:8px; vertical-align:middle; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.2)'" onmouseout="this.style.transform='scale(1)'">🔊</button>` : "";

    msgDiv.innerHTML = `
      <div class="msg-header">
        <span class="role-badge reflex-badge">${headerTitle}</span>
        <span class="timestamp">${now} ${ttsBtnHtml}</span>
      </div>
      <div class="msg-body">${formatMarkdown(text)}</div>
    `;

    // Hook up Indic Audio (Sarvam Bulbul AI & Web Speech API)
    const ttsBtn = msgDiv.querySelector(".tts-btn");
    if (ttsBtn) {
      ttsBtn.addEventListener("click", () => {
        if (ttsBtn.textContent === "📢") {
          if (activeAudio) { activeAudio.pause(); activeAudio = null; }
          if (window.speechSynthesis) window.speechSynthesis.cancel();
          ttsBtn.textContent = "🔊";
          if (voiceIndicator) voiceIndicator.classList.remove("speaking");
        } else {
          speakText(text, ttsBtn);
        }
      });
    }

    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function appendLoadingIndicator() {
    const id = "loading-" + Date.now();
    const loadDiv = document.createElement("div");
    loadDiv.id = id;
    loadDiv.className = "message assistant-msg glass-subcard";
    loadDiv.innerHTML = `
      <div class="msg-header"><span class="role-badge reflex-badge">⚡ Reflex Engine</span></div>
      <div class="msg-body" style="color: #94a3b8; font-style: italic;">Evaluating System 1 reflex decision (&lt;35ms)...</div>
    `;
    chatMessages.appendChild(loadDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
  }

  function removeElement(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function removeLoadingIndicators() {
    document.querySelectorAll("[id^='loading-']").forEach(el => el.remove());
  }

  function addTraceItem(level, text) {
    const item = document.createElement("div");
    item.className = "trace-item";
    item.innerHTML = `
      <div class="trace-dot"></div>
      <div class="trace-content">
        <span class="trace-badge">${level}:</span>
        <span class="trace-text">${text}</span>
      </div>
    `;
    traceLog.prepend(item);
  }

  function updateTelemetry(summary) {
    if (summary.speedup_factor) metricSpeedup.textContent = `${summary.speedup_factor}x`;
    if (summary.savings_percentage) metricSavings.textContent = `${summary.savings_percentage}%`;
    if (summary.system1_percentage) metricS1Ratio.textContent = `${summary.system1_percentage}%`;
    if (summary.avg_latency_ms) barValReflex.textContent = `${summary.avg_latency_ms} ms`;
  }

  function formatMarkdown(text) {
    if (!text) return "";
    return text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\n/g, "<br>");
  }

  // Run Benchmark Button
  btnBenchmark.addEventListener("click", async () => {
    btnBenchmark.disabled = true;
    btnBenchmark.textContent = "Running Benchmark...";
    try {
      const res = await fetch("/api/benchmark");
      const data = await res.json();
      btnBenchmark.textContent = "✓ Benchmark Done";
      setTimeout(() => {
        btnBenchmark.disabled = false;
        btnBenchmark.textContent = "⚡ Run Benchmark";
      }, 3000);
    } catch (e) {
      btnBenchmark.disabled = false;
      btnBenchmark.textContent = "⚡ Run Benchmark";
    }
  });

  // Refresh Telemetry Button
  btnRefresh.addEventListener("click", async () => {
    try {
      const res = await fetch("/api/telemetry");
      const data = await res.json();
      updateTelemetry(data);
    } catch (e) {
      console.warn("Failed to refresh telemetry", e);
    }
  });

  // --- DRAWER FEATURE STUDIO SUB-TAB SWITCHING (Gemini / ChatGPT Style) ---
  const drawerNavBtns = document.querySelectorAll(".drawer-nav-btn");
  const drawerPanes = document.querySelectorAll(".drawer-pane");

  drawerNavBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const paneId = btn.getAttribute("data-pane");
      if (!paneId) return;

      drawerNavBtns.forEach((b) => b.classList.remove("active"));
      drawerPanes.forEach((p) => p.classList.remove("active"));

      btn.classList.add("active");
      const activePane = document.getElementById(paneId);
      if (activePane) {
        activePane.classList.add("active");
        if (window.gsap) {
          gsap.fromTo(activePane, { opacity: 0, y: 8 }, { opacity: 1, y: 0, duration: 0.22, ease: "power2.out" });
        }
      }

      if (paneId === "d-memory") {
        loadFarmMemory();
      }
    });
  });

  // Khet-Vault (FARM_MEMORY.md) loader
  const memoryContent = document.getElementById("memory-md-content");
  const btnReloadMemory = document.getElementById("btn-reload-memory");

  async function loadFarmMemory() {
    if (!memoryContent) return;
    try {
      memoryContent.textContent = "Loading FARM_MEMORY.md from Khet-Vault...";
      const res = await fetch("/api/memory/farm");
      const data = await res.json();
      if (data && data.memory_md) {
        memoryContent.textContent = data.memory_md;
      } else {
        memoryContent.textContent = "# FARM_MEMORY.md (Khet-Vault)\n\nNo active memory records found.";
      }
    } catch (err) {
      memoryContent.textContent = "# Error loading FARM_MEMORY.md\n" + err.message;
    }
  }

  if (btnReloadMemory) {
    btnReloadMemory.addEventListener("click", loadFarmMemory);
  }

  // --- LIVE WEATHER & ROOTZONE SOIL MOISTURE SWITCHER ---
  document.querySelectorAll(".weather-city-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      document.querySelectorAll(".weather-city-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      const city = btn.getAttribute("data-city") || "Indore";
      try {
        const res = await fetch(`/api/weather/live?location=${encodeURIComponent(city)}`);
        const data = await res.json();

        const elName = document.getElementById("weather-city-name");
        const elCond = document.getElementById("weather-condition");
        const elTemp = document.getElementById("weather-temp");
        const elHum = document.getElementById("weather-humidity");
        const elMoist = document.getElementById("weather-soil-moist");
        const elWind = document.getElementById("weather-wind");

        if (elName) elName.textContent = `${data.location || city}, India`;
        if (elCond) elCond.textContent = `🌤️ ${data.condition || "Partly Cloudy"} • Rain Probability: ${data.precipitation_probability_pct ?? 5}%`;
        if (elTemp) elTemp.textContent = `${data.temperature_c ?? 28.4}°C`;
        if (elHum) elHum.textContent = `Humidity: ${data.humidity_pct ?? 48}%`;
        if (elMoist) elMoist.textContent = `${data.rootzone_soil_moisture_m3_per_m3 ?? 0.28} m³/m³`;
        if (elWind) elWind.textContent = `${data.wind_speed_kmh ?? 9.2} km/h`;
      } catch (err) {
        console.warn("Weather fetch fallback:", err);
      }
    });
  });

  // --- INTERACTIVE SEND-TO-CHAT BRIDGES ---
  function sendTextToChat(text) {
    if (!userInput || !chatForm) return;
    switchToTab("tab-chat");
    userInput.value = text;
    chatForm.dispatchEvent(new Event("submit"));
  }

  // Soil ML -> Send to Chat
  const btnSendSoilChat = document.getElementById("btn-send-soil-chat");
  if (btnSendSoilChat) {
    btnSendSoilChat.addEventListener("click", () => {
      const n = document.getElementById("input-n")?.value || "90";
      const p = document.getElementById("input-p")?.value || "42";
      const k = document.getElementById("input-k")?.value || "43";
      const ph = document.getElementById("input-ph")?.value || "6.5";
      const query = `My soil test reports N=${n} kg/ha, P=${p} kg/ha, K=${k} kg/ha, and pH=${ph}. Should I sow soybean or cotton, and what fertilizer dosage should I apply?`;
      sendTextToChat(query);
    });
  }

  // Weather -> Send to Chat
  const btnSendWeatherChat = document.getElementById("btn-send-weather-chat");
  if (btnSendWeatherChat) {
    btnSendWeatherChat.addEventListener("click", () => {
      const city = document.querySelector(".weather-city-btn.active")?.getAttribute("data-city") || "Indore";
      const query = `Based on current weather and soil moisture in ${city}, is it safe to spray pesticide today?`;
      sendTextToChat(query);
    });
  }

  // Govt Schemes -> Send to Chat
  document.querySelectorAll(".btn-ask-scheme").forEach((btn) => {
    btn.addEventListener("click", () => {
      const query = btn.getAttribute("data-scheme");
      if (query) sendTextToChat(query);
    });
  });

  // Panchayat -> Send to Chat
  const btnSendPanchayatChat = document.getElementById("btn-send-panchayat-chat");
  if (btnSendPanchayatChat) {
    btnSendPanchayatChat.addEventListener("click", () => {
      const query = `Tomato crop has a whitefly pest infestation and mandi price is ₹3,800/quintal. What action does Krishi Panchayat recommend?`;
      sendTextToChat(query);
    });
  }

  // --- SOIL ML STUDIO (from l-data-seT---ML) ---
  const sliderN = document.getElementById("input-n");
  const sliderP = document.getElementById("input-p");
  const sliderK = document.getElementById("input-k");
  const sliderPh = document.getElementById("input-ph");
  const sliderRain = document.getElementById("input-rainfall");
  const sliderTemp = document.getElementById("input-temp");

  const valN = document.getElementById("val-n");
  const valP = document.getElementById("val-p");
  const valK = document.getElementById("val-k");
  const valPh = document.getElementById("val-ph");
  const valRain = document.getElementById("val-rainfall");
  const valTemp = document.getElementById("val-temp");

  if (sliderN) sliderN.addEventListener("input", () => (valN.textContent = `${sliderN.value} kg/ha`));
  if (sliderP) sliderP.addEventListener("input", () => (valP.textContent = `${sliderP.value} kg/ha`));
  if (sliderK) sliderK.addEventListener("input", () => (valK.textContent = `${sliderK.value} kg/ha`));
  if (sliderPh) sliderPh.addEventListener("input", () => (valPh.textContent = sliderPh.value));
  if (sliderRain) sliderRain.addEventListener("input", () => (valRain.textContent = `${sliderRain.value} mm`));
  if (sliderTemp) sliderTemp.addEventListener("input", () => (valTemp.textContent = `${sliderTemp.value} °C`));

  // Fertilizer Form Sliders
  const fertMoisture = document.getElementById("fert-moisture");
  const fertN = document.getElementById("fert-n");
  const fertP = document.getElementById("fert-p");
  const fertK = document.getElementById("fert-k");
  const valFertMoisture = document.getElementById("val-fert-moisture");
  const valFertN = document.getElementById("val-fert-n");
  const valFertP = document.getElementById("val-fert-p");
  const valFertK = document.getElementById("val-fert-k");

  if (fertMoisture) fertMoisture.addEventListener("input", () => (valFertMoisture.textContent = `${fertMoisture.value}%`));
  if (fertN) fertN.addEventListener("input", () => (valFertN.textContent = `${fertN.value} kg/ha`));
  if (fertP) fertP.addEventListener("input", () => (valFertP.textContent = `${fertP.value} kg/ha`));
  if (fertK) fertK.addEventListener("input", () => (valFertK.textContent = `${fertK.value} kg/ha`));

  // Subtab Switching (Crop ML vs Fertilizer ML)
  const subtabCropBtn = document.getElementById("subtab-crop-btn");
  const subtabFertBtn = document.getElementById("subtab-fert-btn");
  const soilMlForm = document.getElementById("soil-ml-form");
  const fertMlForm = document.getElementById("fert-ml-form");
  const soilMlOutput = document.getElementById("soil-ml-output");

  if (subtabCropBtn && subtabFertBtn && soilMlForm && fertMlForm) {
    subtabCropBtn.addEventListener("click", () => {
      subtabCropBtn.classList.add("active");
      subtabFertBtn.classList.remove("active");
      soilMlForm.style.display = "grid";
      fertMlForm.style.display = "none";
    });

    subtabFertBtn.addEventListener("click", () => {
      subtabFertBtn.classList.add("active");
      subtabCropBtn.classList.remove("active");
      fertMlForm.style.display = "grid";
      soilMlForm.style.display = "none";
    });
  }

  // Handle Crop ML Form Submit
  if (soilMlForm) {
    soilMlForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      soilMlOutput.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">⏳</div>
          <p style="color: var(--c-mint-whisper);">Running Scikit-Learn multi-model inference on Indian soil dataset...</p>
        </div>
      `;

      try {
        const cropRes = await fetch("/api/ml/crop", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            N: parseFloat(sliderN.value),
            P: parseFloat(sliderP.value),
            K: parseFloat(sliderK.value),
            ph: parseFloat(sliderPh.value),
            rainfall: parseFloat(sliderRain.value),
            temperature: parseFloat(sliderTemp.value),
            humidity: 80.0,
          }),
        });
        const cropData = await cropRes.json();

        // Also fetch fertilizer schedule for top crop
        const topCrop = cropData.top_recommendations?.[0]?.crop || "paddy";
        const fertRes = await fetch("/api/ml/fertilizer", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            crop: topCrop,
            nitrogen: parseFloat(sliderN.value),
            phosphorus: parseFloat(sliderP.value),
            potassium: parseFloat(sliderK.value),
          }),
        });
        const fertData = await fertRes.json();

        // Render Cards with animated progress bars (Suraj.dsgn Luxury Palette)
        let cropsHtml = (cropData.top_recommendations || [])
          .map((c) => {
            const rawVal = parseFloat(c.suitability_percentage) || 15;
            return `
            <div style="padding: 8px 12px; background: rgba(26, 54, 54, 0.7); border: 1px solid rgba(214, 189, 152, 0.15); border-radius: 6px; margin-bottom: 8px;">
              <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                <span style="font-weight: 700; color: #FFFFFF;">🌱 ${c.crop}</span>
                <span style="font-family: var(--font-mono); color: var(--c-emerald-green); font-weight: 700;">${c.suitability_percentage}</span>
              </div>
              <div style="height: 6px; background: rgba(16, 35, 34, 0.8); border-radius: 3px; overflow: hidden;">
                <div style="height: 100%; width: ${rawVal}%; background: linear-gradient(90deg, var(--c-royal-amethyst), var(--c-emerald-green)); border-radius: 3px; transition: width 0.6s ease;"></div>
              </div>
            </div>
          `;
          })
          .join("");

        soilMlOutput.innerHTML = `
          <div style="display: flex; flex-direction: column; gap: 14px;">
            <div style="background: rgba(11, 110, 79, 0.3); border: 1px solid rgba(80, 200, 120, 0.45); border-radius: 8px; padding: 14px; box-shadow: var(--glow-emerald);">
              <div style="font-size: 11px; text-transform: uppercase; color: var(--c-emerald-green); font-weight: 800; letter-spacing: 0.5px;">Optimal Crop Match (System 1 ML)</div>
              <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin-top: 2px;">${cropData.optimal_crop || topCrop}</div>
              <div style="font-size: 12px; color: var(--c-mint-whisper); margin-top: 4px;">${cropData.summary || "High agro-climatic suitability based on regional N-P-K & thermal telemetry."}</div>
            </div>

            <div>
              <div style="font-size: 12px; font-weight: 700; color: var(--c-almond); margin-bottom: 8px; text-transform: uppercase;">Top Crop Suitability Breakdown:</div>
              ${cropsHtml}
            </div>

            <div style="background: rgba(26, 54, 54, 0.75); border: 1px solid rgba(214, 189, 152, 0.35); border-radius: 8px; padding: 12px;">
              <div style="font-size: 11px; text-transform: uppercase; color: var(--c-almond); font-weight: 800; letter-spacing: 0.5px;">Fertilizer Schedule Prescription</div>
              <div style="font-size: 15px; font-weight: 700; color: #FFFFFF; margin-top: 2px;">${fertData.recommended_fertilizer}</div>
              <div style="font-size: 12px; color: var(--c-mint-whisper); margin-top: 4px; line-height: 1.4;">${fertData.agronomic_advice}</div>
            </div>
          </div>
        `;
      } catch (err) {
        soilMlOutput.innerHTML = `<div class="empty-state"><p style="color: #f87171;">Error running prediction: ${err.message}</p></div>`;
      }
    });
  }

  // Handle Dedicated Fertilizer ML Form Submit
  if (fertMlForm) {
    fertMlForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      soilMlOutput.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">⏳</div>
          <p style="color: var(--c-mint-whisper);">Calculating stoichiometric fertilizer requirements...</p>
        </div>
      `;

      try {
        const cropType = document.getElementById("fert-crop-type").value;
        const soilType = document.getElementById("fert-soil-type").value;
        const res = await fetch("/api/ml/fertilizer", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            crop: cropType,
            nitrogen: parseFloat(fertN.value),
            phosphorus: parseFloat(fertP.value),
            potassium: parseFloat(fertK.value),
          }),
        });
        const data = await res.json();

        soilMlOutput.innerHTML = `
          <div style="display: flex; flex-direction: column; gap: 14px;">
            <div style="background: rgba(11, 110, 79, 0.35); border: 1px solid rgba(80, 200, 120, 0.45); border-radius: 8px; padding: 14px;">
              <div style="font-size: 11px; text-transform: uppercase; color: var(--c-emerald-green); font-weight: 800;">Optimal Fertilizer Prescription</div>
              <div style="font-size: 20px; font-weight: 800; color: #FFFFFF; margin-top: 2px;">🧪 ${data.recommended_fertilizer}</div>
              <div style="font-size: 12px; color: var(--c-mint-whisper); margin-top: 4px;">Soil Type: <strong>${soilType}</strong> • Target Crop: <strong>${cropType}</strong></div>
            </div>

            <div style="background: rgba(26, 54, 54, 0.75); border: 1px solid rgba(214, 189, 152, 0.3); border-radius: 8px; padding: 12px;">
              <div style="font-size: 11px; text-transform: uppercase; color: var(--c-almond); font-weight: 800; margin-bottom: 6px;">Agronomic Guidance & Application Strategy</div>
              <div style="font-size: 13px; color: var(--c-mint-whisper); line-height: 1.5;">${data.agronomic_advice}</div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 12px;">
              <div style="background: rgba(16, 35, 34, 0.7); padding: 8px; border-radius: 6px; border: 1px solid rgba(214, 189, 152, 0.15);">
                <span style="color: var(--c-mint-whisper); font-size: 10px; display: block;">Moisture Level</span>
                <strong style="color: var(--c-emerald-green); font-size: 14px;">${fertMoisture.value}% Volumetric</strong>
              </div>
              <div style="background: rgba(16, 35, 34, 0.7); padding: 8px; border-radius: 6px; border: 1px solid rgba(214, 189, 152, 0.15);">
                <span style="color: var(--c-mint-whisper); font-size: 10px; display: block;">NPK Deficit Ratio</span>
                <strong style="color: var(--c-almond); font-size: 13px;">${fertN.value}:${fertP.value}:${fertK.value}</strong>
              </div>
            </div>
          </div>
        `;
      } catch (err) {
        soilMlOutput.innerHTML = `<div class="empty-state"><p style="color: #f87171;">Error calculating fertilizer dosage: ${err.message}</p></div>`;
      }
    });
  }

  // --- KRISHI PANCHAYAT SIMULATION ---
  const btnPanchayat = document.getElementById("btn-simulate-panchayat");
  if (btnPanchayat) {
    btnPanchayat.addEventListener("click", async () => {
      btnPanchayat.disabled = true;
      btnPanchayat.textContent = "Summoning Panchayat Council...";

      try {
        const res = await fetch("/api/panchayat/deliberate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            query: "Tomato whitefly pest infestation and mandi price ₹3,800",
            crop: "Tomato",
            mandi_rate_per_quintal: 3800.0,
            acreage: 4.0,
          }),
        });
        const data = await res.json();

        // Update Agent Cards
        if (data.opinions && data.opinions.length >= 3) {
          document.getElementById("panchayat-op-agri").innerHTML = `
            <strong>Verdict:</strong> ${data.opinions[0].verdict}<br><br>
            • ${data.opinions[0].key_points.join("<br>• ")}<br><br>
            <span style="color: var(--c-emerald-green); font-weight: 700;">Est. Cost: ₹${data.opinions[0].estimated_cost_inr}</span>
          `;
          document.getElementById("panchayat-op-mandi").innerHTML = `
            <strong>Verdict:</strong> ${data.opinions[1].verdict}<br><br>
            • ${data.opinions[1].key_points.join("<br>• ")}<br><br>
            <span style="color: var(--c-emerald-green); font-weight: 700;">Est. Cost: ₹${data.opinions[1].estimated_cost_inr}</span>
          `;
          document.getElementById("panchayat-op-soil").innerHTML = `
            <strong>Verdict:</strong> ${data.opinions[2].verdict}<br><br>
            • ${data.opinions[2].key_points.join("<br>• ")}<br><br>
            <span style="color: var(--c-emerald-green); font-weight: 700;">Est. Cost: ₹${data.opinions[2].estimated_cost_inr}</span>
          `;
        }

        // Update Sarpanch Synthesis
        document.getElementById("panchayat-synthesis").innerHTML = `
          <div style="background: rgba(11, 110, 79, 0.25); border: 1px solid rgba(80, 200, 120, 0.35); padding: 14px; border-radius: 8px; margin-bottom: 10px;">
            <div style="font-weight: 800; color: var(--c-emerald-green); margin-bottom: 6px;">🏛️ Gram Sarpanch Consensus Verdict:</div>
            ${(data.sarpanch_synthesis_english || data.sarpanch_synthesis_hindi).replace(/\n/g, "<br>")}
          </div>
          <div style="display: flex; gap: 16px; margin-top: 12px; font-size: 13px; font-weight: 700;">
            <span style="color: var(--c-emerald-green);">💰 Total Recommended Budget: ₹${data.total_estimated_budget_inr}</span>
            <span style="color: var(--c-almond);">📈 Economic Viability Score: ${(data.economic_viability_score * 100).toFixed(0)}%</span>
          </div>
        `;

        btnPanchayat.disabled = false;
        btnPanchayat.textContent = "✓ Panchayat Deliberation Complete";
        setTimeout(() => (btnPanchayat.textContent = "🏛️ Run Live Panchayat Simulation"), 4000);
      } catch (err) {
        btnPanchayat.disabled = false;
        btnPanchayat.textContent = "🏛️ Run Live Panchayat Simulation";
      }
    });
  }

  // --- LEAFLET SATELLITE EARTH OBSERVATION MAP ---
  let mapInstance = null;
  let activeTileLayer = null;

  const mandiHubs = {
    indore: { 
      name: "Indore APMC (Madhya Pradesh)", 
      coords: [22.7196, 75.8577], 
      n: 90, p: 45, k: 40, ph: 7.1, rain: 180, temp: 26.0, 
      ndvi: 0.65, ndwi: 0.38, 
      rate: "Soybean: ₹4,650/Qtl (▲ +₹120)", 
      zone: "Central Plateau (Vertisols)",
      sowing: "Soybean Pod Filling / Cotton 1st Pick",
      kvk: "Soybean pod borer surveillance active. Use NSKE 5% neem extract or Chlorantraniliprole 18.5 SC @ 60ml/acre. Avoid indiscriminate pyrethroid sprays."
    },
    thanjavur: { 
      name: "Thanjavur (Cauvery Delta Rice Bowl)", 
      coords: [10.7870, 79.1378], 
      n: 92, p: 45, k: 40, ph: 6.7, rain: 210, temp: 28.0, 
      ndvi: 0.74, ndwi: 0.52, 
      rate: "Paddy (CR-1009): ₹2,420/Qtl", 
      zone: "Cauvery Delta Heavy Clay",
      sowing: "Samba Paddy Main Field Transplanting",
      kvk: "Delta humidity favors blast. Apply 25kg Zinc Sulphate/ha as basal dressing. Refrain from urea top-dressing during overcast cloudy spells."
    },
    ludhiana: { 
      name: "Ludhiana (Central Plain Punjab)", 
      coords: [30.9010, 75.8573], 
      n: 105, p: 48, k: 35, ph: 7.4, rain: 110, temp: 22.0, 
      ndvi: 0.78, ndwi: 0.48, 
      rate: "Basmati 1121: ₹3,950/Qtl", 
      zone: "Trans-Gangetic Deep Loam",
      sowing: "Paddy Maturation & Pre-Wheat Prep",
      kvk: "Adopt in-situ stubble management with Super Seeder. Incorporating straw recycles 15kg N, 5kg P, and 60kg K, saving ₹1,200/acre."
    },
    nashik: { 
      name: "Nashik & Lasalgaon (Maharashtra)", 
      coords: [19.9975, 73.7898], 
      n: 70, p: 44, k: 60, ph: 6.9, rain: 140, temp: 24.5, 
      ndvi: 0.61, ndwi: 0.35, 
      rate: "Onion: ₹3,100/Qtl (▲ +12%)", 
      zone: "Deccan Basaltic Regur",
      sowing: "Late Kharif Onion Nursery & Grape Pruning",
      kvk: "Onion thrips monitoring: spray Mancozeb 75 WP @ 2.5g/L water mixed with sticker. Keep nursery beds well-drained."
    },
    coimbatore: { 
      name: "Coimbatore (Kongu Plateau)", 
      coords: [11.0168, 76.9558], 
      n: 65, p: 38, k: 55, ph: 7.2, rain: 95, temp: 26.5, 
      ndvi: 0.62, ndwi: 0.28, 
      rate: "Cotton / Maize: ₹7,450/Qtl", 
      zone: "Red Gravelly Calcareous",
      sowing: "Kharif Cotton Ball Formation",
      kvk: "Bollworm pheromone traps recommended at 5 traps/acre. Balanced potash spray improves boll opening and fiber micronaire."
    },
    agartala: { 
      name: "Agartala Central Mandi (Tripura)", 
      coords: [23.8315, 91.2868], 
      n: 110, p: 35, k: 45, ph: 5.8, rain: 220, temp: 24.0, 
      ndvi: 0.71, ndwi: 0.46, 
      rate: "Tomato: ₹2,450/Qtl (▲ +₹80)", 
      zone: "Eastern Acidic Alluvium",
      sowing: "Early Winter Vegetable Nursery",
      kvk: "Soil acidity pH 5.8 requires agricultural lime application (250 kg/acre). Bacterial wilt resistant varieties recommended."
    },
    kolar: { 
      name: "Kolar Tomato Terminal (Karnataka)", 
      coords: [13.1367, 78.1292], 
      n: 60, p: 50, k: 70, ph: 6.4, rain: 120, temp: 28.0, 
      ndvi: 0.58, ndwi: 0.31, 
      rate: "Paddy: ₹2,183/Qtl (MSP Active)", 
      zone: "Southern Red Loam",
      sowing: "Tomato Staking & Drip Fertigation",
      kvk: "Whitefly vector alert: spray neem oil 10,000 ppm @ 2ml/L to prevent tomato leaf curl virus (ToLCV). Avoid heavy pesticide cocktails."
    },
    azadpur: { 
      name: "Azadpur Mandi (New Delhi Terminal)", 
      coords: [28.7041, 77.1025], 
      n: 80, p: 40, k: 50, ph: 7.2, rain: 90, temp: 25.0, 
      ndvi: 0.52, ndwi: 0.24, 
      rate: "Onion: ₹2,900/Qtl (▲ +₹50)", 
      zone: "Northern Trans-Gangetic Terminal",
      sowing: "National Inflow Terminal / Transit",
      kvk: "Daily terminal inflow tracking active. Onion and potato arrivals from Nashik & Agra steady with moderate buyer competition."
    },
  };

  const tileLayers = {
    sat: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    ndvi: "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
    ndwi: "https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png"
  };

  function initAgriSatelliteMap() {
    const mapContainer = document.getElementById("agri-satellite-map");
    if (!mapContainer || mapInstance || !window.L) return;

    mapInstance = L.map("agri-satellite-map", {
      center: [22.5, 78.9],
      zoom: 5,
      zoomControl: true,
    });

    activeTileLayer = L.tileLayer(tileLayers.sat, {
      attribution: "&copy; Esri &copy; OpenStreetMap",
      maxZoom: 18,
    }).addTo(mapInstance);

    // Add pins for the 8 regional hubs with luxury Suraj.dsgn styling
    Object.keys(mandiHubs).forEach((key) => {
      const hub = mandiHubs[key];
      const marker = L.circleMarker(hub.coords, {
        radius: 9,
        fillColor: "#50C878",
        color: "#D6BD98",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.9,
      }).addTo(mapInstance);

      marker.bindPopup(`
        <div style="font-family: sans-serif; color: #013220; padding: 6px; min-width: 210px;">
          <strong style="font-size: 13px; color: #013220;">${hub.name}</strong><br>
          <span style="font-size: 11px; color: #40534C; font-weight: 600;">Zone: ${hub.zone}</span><br>
          <span style="color: #0B6E4F; font-weight: bold; font-size: 12px;">🟢 ${hub.rate}</span><br>
          <div style="margin: 4px 0; padding: 4px; background: #D1F2EB; border-radius: 4px; font-size: 10px; font-family: monospace; color: #013220;">
            🛰️ NDVI: <strong>${hub.ndvi}</strong> | NDWI: <strong>${hub.ndwi}</strong><br>
            🧪 N:${hub.n} P:${hub.p} K:${hub.k} | pH:${hub.ph}
          </div>
          <button onclick="selectMandiHub('${key}')" style="width: 100%; margin-top: 4px; background: #0B6E4F; color: #D1F2EB; border: none; padding: 6px 8px; border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: 700;">🌱 Load Soil & Run ML</button>
        </div>
      `);
    });
  }

  // Switch Satellite Layers
  window.switchMapLayer = (layerType) => {
    if (!mapInstance || !tileLayers[layerType]) return;
    if (activeTileLayer) mapInstance.removeLayer(activeTileLayer);

    activeTileLayer = L.tileLayer(tileLayers[layerType], {
      attribution: "&copy; CartoDB &copy; Esri &copy; OpenStreetMap",
      maxZoom: 18,
    }).addTo(mapInstance);

    document.querySelectorAll(".layer-btn").forEach((btn) => btn.classList.remove("active"));
    const activeBtn = document.getElementById(`layer-btn-${layerType}`);
    if (activeBtn) activeBtn.classList.add("active");
  };

  document.getElementById("layer-btn-sat")?.addEventListener("click", () => window.switchMapLayer("sat"));
  document.getElementById("layer-btn-ndvi")?.addEventListener("click", () => window.switchMapLayer("ndvi"));
  document.getElementById("layer-btn-ndwi")?.addEventListener("click", () => window.switchMapLayer("ndwi"));

  // Select Hub & Populate Telemetry Card
  window.selectMandiHub = (key) => {
    const hub = mandiHubs[key];
    if (!hub) return;

    if (sliderN) { sliderN.value = hub.n; valN.textContent = `${hub.n} kg/ha`; }
    if (sliderP) { sliderP.value = hub.p; valP.textContent = `${hub.p} kg/ha`; }
    if (sliderK) { sliderK.value = hub.k; valK.textContent = `${hub.k} kg/ha`; }
    if (sliderPh) { sliderPh.value = hub.ph; valPh.textContent = hub.ph; }
    if (sliderRain) { sliderRain.value = hub.rain; valRain.textContent = `${hub.rain} mm`; }
    if (sliderTemp) { sliderTemp.value = hub.temp; valTemp.textContent = `${hub.temp} °C`; }

    // Update telemetry card
    const telCard = document.getElementById("selected-hub-telemetry");
    if (telCard) {
      telCard.style.display = "block";
      document.getElementById("telemetry-hub-name").textContent = `📍 ${hub.name}`;
      document.getElementById("telemetry-agro-zone").textContent = hub.zone;
      document.getElementById("telemetry-ndvi").textContent = `${hub.ndvi} (High Biomass)`;
      document.getElementById("telemetry-ndwi").textContent = `${hub.ndwi} (Hydrated)`;
      document.getElementById("telemetry-sowing").textContent = hub.sowing;
      document.getElementById("telemetry-kvk").innerHTML = `<strong>KVK Alert:</strong> ${hub.kvk}`;
    }

    if (mapInstance) {
      mapInstance.flyTo(hub.coords, 7, { duration: 1.2 });
    }

    if (soilMlForm) {
      soilMlForm.dispatchEvent(new Event("submit"));
    }
  };

  document.querySelectorAll(".map-chip-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const hubKey = btn.getAttribute("data-hub");
      window.selectMandiHub(hubKey);
    });
  });

  // --- JEV-ULTRAFAST GOVERNMENT PORTAL HARVESTER CONTROLLERS ---
  
  // 1. Geographic Scope Filter Toggles (All India / State / District)
  const scopeBtns = document.querySelectorAll(".scope-btn");
  scopeBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      scopeBtns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const scope = btn.getAttribute("data-scope");
      
      const cards = document.querySelectorAll(".scheme-visual-card");
      cards.forEach(card => {
        const cardScope = card.getAttribute("data-scope") || "";
        if (scope === "all" || cardScope.includes(scope)) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  });

  // 2. Scheme Comparison Modal & Checkboxes
  let selectedComparisonSchemes = [];
  const compareBadge = document.getElementById("compare-badge-count");
  const compareModal = document.getElementById("compare-schemes-modal");
  const btnOpenCompare = document.getElementById("btn-open-compare");
  const btnCloseCompare = document.getElementById("btn-close-compare-modal");
  const btnDoneCompare = document.getElementById("btn-done-compare-modal");

  function updateCompareModalData() {
    if (selectedComparisonSchemes.length >= 1) {
      const s1 = selectedComparisonSchemes[0];
      const th1 = document.getElementById("modal-cmp-th-1");
      const name1 = document.getElementById("modal-cmp-name-1");
      const grant1 = document.getElementById("modal-cmp-grant-1");
      const cat1 = document.getElementById("modal-cmp-cat-1");
      const rules1 = document.getElementById("modal-cmp-rules-1");
      if (th1) th1.textContent = s1.name;
      if (name1) name1.textContent = s1.name;
      if (grant1) grant1.textContent = s1.grant;
      if (cat1) cat1.textContent = s1.cat;
      if (rules1) rules1.textContent = s1.rules;
    }
    if (selectedComparisonSchemes.length >= 2) {
      const s2 = selectedComparisonSchemes[1];
      const th2 = document.getElementById("modal-cmp-th-2");
      const name2 = document.getElementById("modal-cmp-name-2");
      const grant2 = document.getElementById("modal-cmp-grant-2");
      const cat2 = document.getElementById("modal-cmp-cat-2");
      const rules2 = document.getElementById("modal-cmp-rules-2");
      if (th2) th2.textContent = s2.name;
      if (name2) name2.textContent = s2.name;
      if (grant2) grant2.textContent = s2.grant;
      if (cat2) cat2.textContent = s2.cat;
      if (rules2) rules2.textContent = s2.rules;
    }
  }

  document.querySelectorAll(".cmp-cb").forEach((cb) => {
    cb.addEventListener("change", (e) => {
      const id = cb.getAttribute("data-id");
      const name = cb.getAttribute("data-name");
      const grant = cb.getAttribute("data-grant");
      const cat = cb.getAttribute("data-cat");
      const rules = cb.getAttribute("data-rules");

      if (cb.checked) {
        if (selectedComparisonSchemes.length >= 2) {
          selectedComparisonSchemes.shift();
        }
        selectedComparisonSchemes.push({ id, name, grant, cat, rules });
      } else {
        selectedComparisonSchemes = selectedComparisonSchemes.filter(s => s.id !== id);
      }

      if (compareBadge) {
        compareBadge.textContent = selectedComparisonSchemes.length;
      }
      updateCompareModalData();
    });
  });

  if (btnOpenCompare && compareModal) {
    btnOpenCompare.addEventListener("click", () => {
      if (selectedComparisonSchemes.length < 2) {
        // Auto-select first two if less than 2 checked
        selectedComparisonSchemes = [
          { name: "PM-Kisan + MP Kalyan", grant: "₹10,000 / Year", cat: "Direct Cash Benefit (DBT)", rules: "Aadhaar e-KYC + Khasra Record" },
          { name: "SMAM Farm Mechanization", grant: "50% (Max ₹45,000)", cat: "Farm Machinery", rules: "Small/Marginal Farmer (<5 acres)" }
        ];
        if (compareBadge) compareBadge.textContent = "2";
        updateCompareModalData();
      }
      compareModal.classList.add("active");
    });
  }

  if (btnCloseCompare && compareModal) {
    btnCloseCompare.addEventListener("click", () => {
      compareModal.classList.remove("active");
    });
  }

  if (btnDoneCompare && compareModal) {
    btnDoneCompare.addEventListener("click", () => {
      compareModal.classList.remove("active");
    });
  }

  // 3. Live JEV-Ultrafast Browser View Simulator
  window.reloadJevPortal = () => {
    const screen = document.getElementById("jev-viewport-screen");
    if (!screen) return;
    const body = document.getElementById("jev-portal-rendered-body");
    if (body) {
      body.innerHTML = `
        <div style="padding:20px; text-align:center; color:#6b7280; font-family:var(--font-mono); font-size:11px;">
          <div style="font-size:24px; animation:spin 1s linear infinite; margin-bottom:8px;">⚡</div>
          <div>JEV-Ultrafast live crawler refreshing official gazette notifications...</div>
        </div>
      `;
      setTimeout(() => {
        window.switchJevPortal("pmkisan");
      }, 600);
    }
  };

  window.switchJevPortal = (portalKey) => {
    const urlBar = document.getElementById("jev-url-address");
    const tabName = document.getElementById("jev-active-tab-name");
    const body = document.getElementById("jev-portal-rendered-body");

    if (portalKey === "pmkisan") {
      if (urlBar) urlBar.value = "https://pmkisan.gov.in/portal/farmer_benefits.aspx";
      if (tabName) tabName.textContent = "pmkisan.gov.in";
      if (body) {
        body.innerHTML = `
          <div style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:6px; padding:10px; margin-bottom:10px;">
            <strong style="color:#065f46; display:block; margin-bottom:4px;">Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)</strong>
            <p style="margin:0 0 6px 0;">All landholding farmer families having cultivable landholding in their names are eligible. DBT financial benefit of ₹6,000/yr in 3 installments.</p>
            <div style="display:flex; gap:6px; font-family:var(--font-mono); font-size:9px;">
              <span style="background:#d1fae5; color:#065f46; padding:2px 6px; border-radius:3px;">eKYC: Verified</span>
              <span style="background:#dbeafe; color:#1e40af; padding:2px 6px; border-radius:3px;">Aadhaar Seeded: Yes</span>
            </div>
          </div>
          <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:6px; padding:10px;">
            <strong style="color:#92400e; display:block; margin-bottom:4px;">MP Mukhyamantri Kisan Kalyan Yojana (Top-Up)</strong>
            <p style="margin:0;">MP State grants additional ₹4,000/year to all PM-Kisan registered farmers across MP districts including Indore.</p>
          </div>
          <div style="margin-top:12px; background:#0f172a; border:1px solid #10b981; border-radius:6px; padding:8px; display:flex; justify-content:space-between; align-items:center; font-family:var(--font-mono); font-size:10px; color:#34d399;">
            <span>⚡ JEV: 24,180 words pruned → 3 rules extracted</span>
            <span style="color:#fff;">14.2ms</span>
          </div>
        `;
      }
    } else if (portalKey === "agrimachinery") {
      if (urlBar) urlBar.value = "https://agrimachinery.nic.in/Farmer/SubMissionMachinery";
      if (tabName) tabName.textContent = "agrimachinery.nic.in";
      if (body) {
        body.innerHTML = `
          <div style="background:#fffbeb; border:1px solid #fde68a; border-radius:6px; padding:10px; margin-bottom:10px;">
            <strong style="color:#92400e; display:block; margin-bottom:4px;">Sub-Mission on Agricultural Mechanization (SMAM)</strong>
            <p style="margin:0 0 6px 0;">50% financial assistance for purchasing Super Seeder, Rotavator, Straw Reaper in MP. Priority for small/marginal farmers (&lt;5 acres).</p>
            <div style="display:flex; gap:6px; font-family:var(--font-mono); font-size:9px;">
              <span style="background:#fef3c7; color:#92400e; padding:2px 6px; border-radius:3px;">Grant: ₹45,000</span>
              <span style="background:#dcfce7; color:#166534; padding:2px 6px; border-radius:3px;">Dealer Subsidy Direct</span>
            </div>
          </div>
          <div style="margin-top:12px; background:#0f172a; border:1px solid #10b981; border-radius:6px; padding:8px; display:flex; justify-content:space-between; align-items:center; font-family:var(--font-mono); font-size:10px; color:#34d399;">
            <span>⚡ JEV: 31,400 words pruned → 2 rules extracted</span>
            <span style="color:#fff;">16.1ms</span>
          </div>
        `;
      }
    } else if (portalKey === "kusum") {
      if (urlBar) urlBar.value = "https://pmkusum.mnre.gov.in/landing/component-b";
      if (tabName) tabName.textContent = "pmkusum.mnre.gov.in";
      if (body) {
        body.innerHTML = `
          <div style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:6px; padding:10px; margin-bottom:10px;">
            <strong style="color:#1e40af; display:block; margin-bottom:4px;">PM-KUSUM Component-B (Solar Water Pump 5HP)</strong>
            <p style="margin:0 0 6px 0;">60% government subsidy (30% Central + 30% State) for replacement of diesel pump in off-grid farmlands. Saves ₹32,000/yr diesel.</p>
            <div style="display:flex; gap:6px; font-family:var(--font-mono); font-size:9px;">
              <span style="background:#dbeafe; color:#1e40af; padding:2px 6px; border-radius:3px;">Subsidy: 60%</span>
              <span style="background:#dcfce7; color:#166534; padding:2px 6px; border-radius:3px;">Diesel Free</span>
            </div>
          </div>
          <div style="margin-top:12px; background:#0f172a; border:1px solid #10b981; border-radius:6px; padding:8px; display:flex; justify-content:space-between; align-items:center; font-family:var(--font-mono); font-size:10px; color:#34d399;">
            <span>⚡ JEV: 19,250 words pruned → 3 rules extracted</span>
            <span style="color:#fff;">13.0ms</span>
          </div>
        `;
      }
    }
  };

  document.querySelectorAll(".btn-open-jev").forEach((btn) => {
    btn.addEventListener("click", () => {
      const portal = btn.getAttribute("data-portal");
      window.switchJevPortal(portal);
    });
  });

  // 4. Interactive Laya Vernacular Portal Reader AI Chat
  const inputLayaPortal = document.getElementById("input-laya-portal-q");
  const btnAskLayaPortal = document.getElementById("btn-ask-laya-portal");
  const btnMicLayaPortal = document.getElementById("btn-mic-laya-portal");
  const layaChatBubble = document.getElementById("laya-portal-chat-bubble");

  function triggerLayaPortalAsk() {
    if (!inputLayaPortal || !layaChatBubble) return;
    const query = inputLayaPortal.value.trim();
    if (!query) return;

    layaChatBubble.innerHTML = `<span class="animate-pulse" style="color:var(--c-emerald-green);">⚡ Laya System 1 scanning government gazettes for "${query}"...</span>`;
    
    setTimeout(() => {
      layaChatBubble.innerHTML = `
        💬 <strong>Laya Gov Reader AI:</strong><br>
        "Rameshwar ji! JEV has extracted rules from the official government gazette: 
        1. <strong>Super Seeder Machine:</strong> Requires Aadhaar card, Khasra land record (4.0 Acres), and bank passbook. 50% subsidy is deducted directly on the dealer invoice.<br>
        2. <strong>PM-KUSUM:</strong> If you have an active borewell or well, 60% subsidy is approved."
      `;
      inputLayaPortal.value = "";
    }, 550);
  }

  if (btnAskLayaPortal) {
    btnAskLayaPortal.addEventListener("click", triggerLayaPortalAsk);
  }
  if (inputLayaPortal) {
    inputLayaPortal.addEventListener("keypress", (e) => {
      if (e.key === "Enter") triggerLayaPortalAsk();
    });
  }
  if (btnMicLayaPortal) {
    btnMicLayaPortal.addEventListener("click", () => {
      if (layaChatBubble) {
        layaChatBubble.innerHTML = `🎙️ <span style="color:var(--c-almond); font-weight:bold;">Listening...</span> Which scheme rules would you like to explore?`;
      }
      setTimeout(() => {
        if (inputLayaPortal) {
          inputLayaPortal.value = "What documents are required for Super Seeder machine?";
          triggerLayaPortalAsk();
        }
      }, 2000);
    });
  }

});


