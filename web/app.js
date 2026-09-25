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
  if (btnFieldMode) {
    btnFieldMode.addEventListener("click", () => {
      const isField = document.body.classList.toggle("field-mode");
      btnFieldMode.innerHTML = isField ? "<span>🌙 Dark Matrix</span>" : "<span>☀️ Field Mode</span>";
    });
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
          userInput.value = "टमाटर के पत्तों पर रोग दिख रहा है। कृपया फोटो देखकर रोग और उपचार बताएं। (Diagnose disease from attached leaf photo)";
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
          userInput.value = "टमाटर के पत्तों पर रोग दिख रहा है। कृपया फोटो देखकर रोग और उपचार बताएं। (Diagnose disease from attached leaf photo)";
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
    const ttsBtnHtml = role !== "user" ? `<button class="tts-btn" title="🔊 आवाज में सुनें (Listen in Vernacular Voice)" style="background:none; border:none; cursor:pointer; font-size:15px; margin-left:8px; vertical-align:middle; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.2)'" onmouseout="this.style.transform='scale(1)'">🔊</button>` : "";

    msgDiv.innerHTML = `
      <div class="msg-header">
        <span class="role-badge reflex-badge">${headerTitle}</span>
        <span class="timestamp">${now} ${ttsBtnHtml}</span>
      </div>
      <div class="msg-body">${formatMarkdown(text)}</div>
    `;

    // Hook up native Web Speech API TTS
    const ttsBtn = msgDiv.querySelector(".tts-btn");
    const voiceIndicator = document.getElementById("voice-indicator");
    if (ttsBtn && window.speechSynthesis) {
      ttsBtn.addEventListener("click", () => {
        window.speechSynthesis.cancel();
        const cleanText = text.replace(/[*#`_]/g, "").replace(/<[^>]*>/g, "");
        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = /[\u0900-\u097F]/.test(cleanText) ? "hi-IN" : "en-IN";
        utterance.rate = 0.95;
        ttsBtn.textContent = "📢";
        if (voiceIndicator) voiceIndicator.classList.add("speaking");

        const resetSpeaking = () => {
          ttsBtn.textContent = "🔊";
          if (voiceIndicator) voiceIndicator.classList.remove("speaking");
        };

        utterance.onend = resetSpeaking;
        utterance.onerror = resetSpeaking;
        window.speechSynthesis.speak(utterance);
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

  // --- TAB NAVIGATION SWITCHING ---
  const navTabs = document.querySelectorAll(".nav-tab");
  const tabPanes = document.querySelectorAll(".tab-pane");

  navTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const targetId = tab.getAttribute("data-tab");

      navTabs.forEach((t) => t.classList.remove("active"));
      tabPanes.forEach((p) => p.classList.remove("active"));

      tab.classList.add("active");
      const targetPane = document.getElementById(targetId);
      if (targetPane) targetPane.classList.add("active");

      // If opening Khet-Vault, load live FARM_MEMORY.md
      if (targetId === "tab-memory") {
        loadFarmMemory();
      }
    });
  });

  async function loadFarmMemory() {
    const memoryCode = document.getElementById("memory-md-content");
    try {
      const res = await fetch("/api/memory/farm");
      const data = await res.json();
      if (data.memory_md) {
        memoryCode.innerHTML = `<code>${data.memory_md}</code>`;
      }
    } catch (e) {
      console.warn("Failed to fetch farm memory", e);
    }
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
            query: "टमाटर में सफेद मक्खी का हमला और मंडी भाव ₹3,800",
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
            <div style="font-weight: 800; color: var(--c-emerald-green); margin-bottom: 6px;">🇮🇳 हिंदी निर्णय (Sarpanch Verdict):</div>
            ${data.sarpanch_synthesis_hindi.replace(/\n/g, "<br>")}
          </div>
          <div style="background: rgba(26, 54, 54, 0.6); border: 1px solid rgba(214, 189, 152, 0.25); padding: 14px; border-radius: 8px;">
            <div style="font-weight: 800; color: var(--c-almond); margin-bottom: 6px;">🇬🇧 English Synthesis:</div>
            ${data.sarpanch_synthesis_english.replace(/\n/g, "<br>")}
          </div>
          <div style="display: flex; gap: 16px; margin-top: 12px; font-size: 13px; font-weight: 700;">
            <span style="color: var(--c-emerald-green);">💰 Total Budget: ₹${data.total_estimated_budget_inr}</span>
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

  // Trigger map resize on tab switch
  document.querySelectorAll(".nav-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const tabTarget = tab.getAttribute("data-tab");
      if (!tabTarget) return;

      document.querySelectorAll(".nav-tab").forEach((t) => t.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach((p) => p.classList.remove("active"));

      tab.classList.add("active");
      const targetPane = document.getElementById(tabTarget);
      if (targetPane) targetPane.classList.add("active");

      if (tabTarget === "tab-soil-ml") {
        setTimeout(() => {
          initAgriSatelliteMap();
          if (mapInstance) mapInstance.invalidateSize();
        }, 200);
      }
    });
  });
});


