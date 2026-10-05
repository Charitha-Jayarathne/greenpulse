"""
Generate complete modern Node-RED flow for GreenPulse
"""

import json
from pathlib import Path
import requests

FLOW_FILE = Path("f:/greenpulse/node_red_flow.json")

# SVG Icons (React Icons / Lucide style)
SVG_SPROUT = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>"""

SVG_DROPLET = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>"""

SVG_THERMO = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"/></svg>"""

SVG_PROBE = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>"""

SVG_WIND = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.7 7.7a2.5 2.5 0 1 1 1.8 4.3H2"/><path d="M9.6 4.6A2 2 0 1 1 11 8H2"/><path d="M12.6 19.4A2 2 0 1 0 14 16H2"/></svg>"""

SVG_GAUGE = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/></svg>"""

SVG_RAIN = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M16 14v6"/><path d="M8 14v6"/><path d="M12 16v6"/></svg>"""

SVG_MAPPIN = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>"""

SVG_SPARKLES = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>"""

SVG_SETTINGS = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/></svg>"""

SVG_CHECK = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>"""

SVG_ALERT = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>"""

SVG_ACTIVITY = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>"""

SVG_REFRESH = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>"""

SVG_SUN = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>"""

# HTML / CSS / Angular Template
TEMPLATE_HTML = f"""
<div id="gp-app" class="gp-dashboard" ng-init="init()">

  <!-- ================= TOP HEADER ================= -->
  <header class="gp-header">
    <div class="gp-brand">
      <div class="gp-logo-badge">
        {SVG_SPROUT}
      </div>
      <div>
        <div class="gp-title">GreenPulse <span class="gp-accent">IoT Core</span></div>
        <div class="gp-subtitle">Autonomous Botanical Intelligence & Telemetry</div>
      </div>
    </div>

    <div class="gp-header-center">
      <div class="gp-pill gp-pill-device">
        <span class="gp-dot-live"></span>
        <span class="gp-pill-text">ESP32: <strong>{{{{sensor.device_id || 'greenpulse-team-infinix'}}}}</strong></span>
      </div>
      <div class="gp-pill gp-pill-aws">
        <span class="gp-dot-live pulse-emerald"></span>
        <span class="gp-pill-text">AWS IoT Core mTLS (Port 8883)</span>
      </div>
    </div>

    <div class="gp-header-actions">
      <div class="gp-clock">
        <div class="gp-clock-time">{{{{currentTime}}}}</div>
        <div class="gp-clock-zone">Sri Lanka Standard Time</div>
      </div>

      <button class="gp-btn gp-btn-config" ng-click="openConfigModal()">
        {SVG_SETTINGS}
        <span>Change Plant & Location Info</span>
      </button>
    </div>
  </header>

  <!-- ================= ACTIVE PLANT & CITY WEATHER BANNER ================= -->
  <section class="gp-meta-grid">
    <!-- Active Plant Card -->
    <div class="gp-meta-card gp-plant-card">
      <div class="gp-meta-icon-box gp-icon-emerald">
        {SVG_SPROUT}
      </div>
      <div class="gp-meta-info">
        <div class="gp-meta-label">Active Plant Species</div>
        <div class="gp-meta-val-row">
          <span class="gp-meta-title">{{{{plant.plant_name || 'Tomato'}}}}</span>
          <span class="gp-badge gp-badge-emerald">Safe Moisture: {{{{plant.min_moisture}}}}% - {{{{plant.max_moisture}}}}%</span>
        </div>
        <div class="gp-meta-desc">{{{{plant.notes || 'Target botanical parameters actively guarded'}}}}</div>
      </div>
      <button class="gp-mini-btn" ng-click="openConfigModal()">Switch</button>
    </div>

    <!-- Live City Weather Card -->
    <div class="gp-meta-card gp-weather-card">
      <div class="gp-meta-icon-box" ng-class="{{'gp-icon-cyan': weather.rain_expected, 'gp-icon-amber': !weather.rain_expected}}">
        <span ng-if="weather.rain_expected">{SVG_RAIN}</span>
        <span ng-if="!weather.rain_expected">{SVG_SUN}</span>
      </div>
      <div class="gp-meta-info">
        <div class="gp-meta-label">Live City Microclimate ({SVG_MAPPIN} {{{{weather.city || plant.location_name || 'Colombo'}}}})</div>
        <div class="gp-meta-val-row">
          <span class="gp-meta-title">{{{{weather.temp || 26.9}}}} °C</span>
          <span class="gp-weather-cond">{{{{weather.description || 'Scattered Clouds'}}}} • {{{{weather.humidity || 85}}}}% Air Humidity</span>
        </div>
        <div class="gp-rain-status" ng-class="{{'rain-alert': weather.rain_expected, 'rain-clear': !weather.rain_expected}}">
          <span ng-if="weather.rain_expected">{SVG_RAIN} Rain Expected within 24h — Automatic Irrigation Delay Active</span>
          <span ng-if="!weather.rain_expected">{SVG_SUN} Clear Weather Forecast — Standard Botanical Schedule</span>
        </div>
      </div>
      <button class="gp-mini-btn" ng-click="refreshWeather()">{SVG_REFRESH}</button>
    </div>
  </section>

  <!-- ================= 6 SENSOR TELEMETRY CARDS ================= -->
  <section class="gp-sensors-grid">
    <!-- 1. Soil Moisture -->
    <div class="gp-card gp-card-metric" ng-class="{{'border-alert': sensor.soil_moisture < plant.min_moisture, 'border-optimal': sensor.soil_moisture >= plant.min_moisture && sensor.soil_moisture <= plant.max_moisture}}">
      <div class="gp-card-header">
        <span class="gp-card-icon gp-icon-emerald">{SVG_DROPLET}</span>
        <span class="gp-card-tag" ng-class="{{'tag-opt': sensor.soil_moisture >= plant.min_moisture && sensor.soil_moisture <= plant.max_moisture, 'tag-warn': sensor.soil_moisture < plant.min_moisture}}">
          {{{{sensor.soil_moisture >= plant.min_moisture ? 'Optimal Hydration' : 'Water Deficit'}}}}
        </span>
      </div>
      <div class="gp-metric-val">{{{{sensor.soil_moisture | number:1}}}}<span class="gp-unit">%</span></div>
      <div class="gp-metric-name">Soil Moisture (Root Level)</div>
      <div class="gp-bar-track">
        <div class="gp-bar-fill gp-fill-emerald" style="width: {{{{sensor.soil_moisture}}}}%;"></div>
      </div>
      <div class="gp-range-hint">Safe Band: {{{{plant.min_moisture}}}}% – {{{{plant.max_moisture}}}}%</div>
    </div>

    <!-- 2. Soil Temperature (DS18B20) -->
    <div class="gp-card gp-card-metric">
      <div class="gp-card-header">
        <span class="gp-card-icon gp-icon-teal">{SVG_PROBE}</span>
        <span class="gp-card-tag tag-opt">Sub-surface Probe</span>
      </div>
      <div class="gp-metric-val">{{{{sensor.soil_temperature | number:1}}}}<span class="gp-unit">°C</span></div>
      <div class="gp-metric-name">Soil Temperature (DS18B20)</div>
      <div class="gp-bar-track">
        <div class="gp-bar-fill gp-fill-teal" style="width: {{{{ (sensor.soil_temperature / 45) * 100 }}}}%;"></div>
      </div>
      <div class="gp-range-hint">Target Range: 18.0°C – 28.0°C</div>
    </div>

    <!-- 3. Ambient Temperature (DHT22) -->
    <div class="gp-card gp-card-metric">
      <div class="gp-card-header">
        <span class="gp-card-icon gp-icon-amber">{SVG_THERMO}</span>
        <span class="gp-card-tag" ng-class="{{'tag-opt': sensor.temperature <= 32, 'tag-warn': sensor.temperature > 32}}">
          {{{{sensor.temperature <= 32 ? 'Comfort Zone' : 'Heat Warning'}}}}
        </span>
      </div>
      <div class="gp-metric-val">{{{{sensor.temperature | number:1}}}}<span class="gp-unit">°C</span></div>
      <div class="gp-metric-name">Ambient Temperature (DHT22)</div>
      <div class="gp-bar-track">
        <div class="gp-bar-fill gp-fill-amber" style="width: {{{{ (sensor.temperature / 45) * 100 }}}}%;"></div>
      </div>
      <div class="gp-range-hint">Threshold Ceiling: 33.0°C</div>
    </div>

    <!-- 4. Ambient Humidity (DHT22) -->
    <div class="gp-card gp-card-metric">
      <div class="gp-card-header">
        <span class="gp-card-icon gp-icon-blue">{SVG_DROPLET}</span>
        <span class="gp-card-tag tag-opt">Transpiration Comfort</span>
      </div>
      <div class="gp-metric-val">{{{{sensor.humidity | number:1}}}}<span class="gp-unit">%</span></div>
      <div class="gp-metric-name">Relative Humidity (DHT22)</div>
      <div class="gp-bar-track">
        <div class="gp-bar-fill gp-fill-blue" style="width: {{{{sensor.humidity}}}}%;"></div>
      </div>
      <div class="gp-range-hint">Optimal Range: 40% – 70%</div>
    </div>

    <!-- 5. Air Quality MQ Sensor -->
    <div class="gp-card gp-card-metric">
      <div class="gp-card-header">
        <span class="gp-card-icon gp-icon-cyan">{SVG_WIND}</span>
        <span class="gp-card-tag tag-opt">Clean Air Level</span>
      </div>
      <div class="gp-metric-val">{{{{sensor.air_quality_percent | number:0}}}}<span class="gp-unit">%</span></div>
      <div class="gp-metric-name">Air Purity & Gas Sensor</div>
      <div class="gp-bar-track">
        <div class="gp-bar-fill gp-fill-cyan" style="width: {{{{sensor.air_quality_percent}}}}%;"></div>
      </div>
      <div class="gp-range-hint">Indoor / Outdoor Air Quality: 100% Clean</div>
    </div>

    <!-- 6. Barometric Pressure (BMP280) -->
    <div class="gp-card gp-card-metric">
      <div class="gp-card-header">
        <span class="gp-card-icon gp-icon-purple">{SVG_GAUGE}</span>
        <span class="gp-card-tag tag-opt">BMP280 I2C</span>
      </div>
      <div class="gp-metric-val">{{{{sensor.air_pressure | number:1}}}}<span class="gp-unit">hPa</span></div>
      <div class="gp-metric-name">Barometric Pressure</div>
      <div class="gp-bar-track">
        <div class="gp-bar-fill gp-fill-purple" style="width: {{{{ ((sensor.air_pressure - 950) / 100) * 100 }}}}%;"></div>
      </div>
      <div class="gp-range-hint">Standard Atmosphere: ~1013.25 hPa</div>
    </div>
  </section>

  <!-- ================= HEALTH STATUS & AI DOCTOR ROW ================= -->
  <section class="gp-intelligence-grid">
    <!-- Physical Hardware LED Simulator & Priority Card -->
    <div class="gp-card gp-health-card">
      <div class="gp-intel-header">
        <div class="gp-intel-title-row">
          <span class="gp-intel-icon gp-icon-emerald">{SVG_ACTIVITY}</span>
          <div>
            <div class="gp-intel-title">Plant Health & Priority LEDs</div>
            <div class="gp-intel-sub">Hardware Priority Indicators (ESP32 Pins 25, 26, 27)</div>
          </div>
        </div>
      </div>

      <!-- Glowing Physical LEDs -->
      <div class="gp-led-bar">
        <div class="gp-led-item" ng-class="{{'active-red': statusLed === 'RED'}}">
          <div class="gp-led-bulb bulb-red"></div>
          <div class="gp-led-label">RED LED<br><span>Pin 25 (Critical)</span></div>
        </div>
        <div class="gp-led-item" ng-class="{{'active-yellow': statusLed === 'YELLOW'}}">
          <div class="gp-led-bulb bulb-yellow"></div>
          <div class="gp-led-label">YELLOW LED<br><span>Pin 26 (Warning)</span></div>
        </div>
        <div class="gp-led-item" ng-class="{{'active-green': statusLed === 'GREEN'}}">
          <div class="gp-led-bulb bulb-green"></div>
          <div class="gp-led-label">GREEN LED<br><span>Pin 27 (Optimal)</span></div>
        </div>
      </div>

      <!-- Status Verdict -->
      <div class="gp-status-box" ng-class="{{'status-green': statusLed === 'GREEN', 'status-yellow': statusLed === 'YELLOW', 'status-red': statusLed === 'RED'}}">
        <div class="gp-status-head">
          <span ng-if="statusLed === 'GREEN'">{SVG_CHECK}</span>
          <span ng-if="statusLed !== 'GREEN'">{SVG_ALERT}</span>
          <span>{{{{healthTitle || 'HEALTHY CONDITION DETECTED'}}}}</span>
        </div>
        <div class="gp-status-msg">{{{{healthMessage || 'All 6 microclimate telemetry metrics reside inside target boundaries.'}}}}</div>
      </div>

      <!-- Simulation Inject Bar -->
      <div class="gp-sim-bar">
        <div class="gp-sim-title">One-Click Demonstration Simulations:</div>
        <div class="gp-sim-btns">
          <button class="gp-btn-sim sim-opt" ng-click="injectTest('healthy')">Healthy Plant</button>
          <button class="gp-btn-sim sim-dry" ng-click="injectTest('dry')">Dry Soil Alert</button>
          <button class="gp-btn-sim sim-hot" ng-click="injectTest('hot')">Heat Stress (34°C)</button>
          <button class="gp-btn-sim sim-rain" ng-click="injectTest('rain')">Rain Incoming</button>
        </div>
      </div>
    </div>

    <!-- Gemini AI Plant Care Doctor Card -->
    <div class="gp-card gp-ai-card">
      <div class="gp-intel-header">
        <div class="gp-intel-title-row">
          <span class="gp-intel-icon gp-icon-sparkle">{SVG_SPARKLES}</span>
          <div>
            <div class="gp-intel-title">Gemini 3.8 Flash Plant Doctor</div>
            <div class="gp-intel-sub">Synthesizing Sensors + {{{{plant.plant_name}}}} + {{{{weather.city}}}} Weather</div>
          </div>
        </div>

        <button class="gp-btn gp-btn-ai-run" ng-click="runAiDiagnosis()" ng-disabled="aiLoading">
          <span ng-if="!aiLoading">{SVG_SPARKLES}</span>
          <span ng-if="aiLoading" class="gp-spin">{SVG_REFRESH}</span>
          <span>{{{{aiLoading ? 'Consulting Gemini AI...' : 'Run Gemini AI Diagnosis'}}}}</span>
        </button>
      </div>

      <!-- AI Diagnosis Result -->
      <div class="gp-ai-content">
        <div ng-if="aiLoading" class="gp-ai-loading-box">
          <div class="gp-pulse-ring"></div>
          <div class="gp-loading-text">Analyzing multi-sensor telemetry, soil thermal conductivity, and Colombo rain forecast...</div>
        </div>

        <div ng-if="!aiLoading" class="gp-ai-markdown" ng-bind-html="aiAdviceHtml"></div>
      </div>

      <div class="gp-ai-footer">
        <span>Model: Google Gemini 3.8 Flash</span>
        <span>Decision Engine: Active</span>
        <span>Telemetry Latency: &lt; 10s</span>
      </div>
    </div>
  </section>

  <!-- ================= REAL-TIME TRENDS CHART ================= -->
  <section class="gp-chart-section">
    <div class="gp-card gp-chart-card">
      <div class="gp-chart-header">
        <div class="gp-chart-title-row">
          <span class="gp-intel-icon gp-icon-teal">{SVG_ACTIVITY}</span>
          <div>
            <div class="gp-intel-title">Multi-Sensor Telemetry Trends</div>
            <div class="gp-intel-sub">Live 60-Second Realtime Sensor Telemetry Stream</div>
          </div>
        </div>

        <div class="gp-chart-legend">
          <span class="gp-legend-item"><span class="dot-emerald"></span> Soil Moisture (%)</span>
          <span class="gp-legend-item"><span class="dot-teal"></span> Soil Temp (°C)</span>
          <span class="gp-legend-item"><span class="dot-amber"></span> Ambient Temp (°C)</span>
          <span class="gp-legend-item"><span class="dot-blue"></span> Air Humidity (%)</span>
        </div>
      </div>

      <div class="gp-chart-canvas-wrap">
        <canvas id="gpTelemetryChart" height="240"></canvas>
      </div>
    </div>
  </section>

  <!-- ================= CONFIGURATION MODAL ================= -->
  <div class="gp-modal-backdrop" ng-if="showConfigModal" ng-click="closeConfigModal($event)">
    <div class="gp-modal-content" ng-click="$event.stopPropagation()">
      <div class="gp-modal-header">
        <div class="gp-modal-title-row">
          <span class="gp-icon-emerald">{SVG_SETTINGS}</span>
          <h3>Plant Profile & Location Settings</h3>
        </div>
        <button class="gp-modal-close" ng-click="closeConfigModal()">✕</button>
      </div>

      <div class="gp-modal-body">
        <!-- Preset Selector Buttons -->
        <div class="gp-form-group">
          <label class="gp-form-label">Botanical Species Preset:</label>
          <div class="gp-preset-chips">
            <button type="button" class="gp-chip" ng-repeat="(name, preset) in presets" ng-class="{{'chip-active': tempConfig.plant_name === name}}" ng-click="selectPreset(name, preset)">
              {{{{name}}}}
            </button>
          </div>
        </div>

        <div class="gp-form-row">
          <div class="gp-form-group gp-col-6">
            <label class="gp-form-label">Plant Name / Species:</label>
            <input type="text" class="gp-input" ng-model="tempConfig.plant_name" placeholder="e.g. Tomato, Rose, Monstera">
          </div>

          <div class="gp-form-group gp-col-6">
            <label class="gp-form-label">City / Weather Location:</label>
            <input type="text" class="gp-input" ng-model="tempConfig.location_name" placeholder="e.g. Colombo, Kandy, Galle">
          </div>
        </div>

        <!-- Quick City Selector -->
        <div class="gp-form-group">
          <label class="gp-form-label">Quick City Presets (Sri Lanka):</label>
          <div class="gp-city-chips">
            <button type="button" class="gp-chip-sm" ng-repeat="city in quickCities" ng-class="{{'chip-active': tempConfig.location_name === city}}" ng-click="tempConfig.location_name = city">
              {{{{city}}}}
            </button>
          </div>
        </div>

        <div class="gp-form-row">
          <div class="gp-form-group gp-col-6">
            <label class="gp-form-label">Min Safe Soil Moisture (%):</label>
            <input type="number" class="gp-input" ng-model="tempConfig.min_moisture" min="5" max="95">
          </div>

          <div class="gp-form-group gp-col-6">
            <label class="gp-form-label">Max Safe Soil Moisture (%):</label>
            <input type="number" class="gp-input" ng-model="tempConfig.max_moisture" min="10" max="100">
          </div>
        </div>

        <div class="gp-form-group">
          <label class="gp-form-label">Botanical Growth Notes:</label>
          <textarea class="gp-input gp-textarea" ng-model="tempConfig.notes" rows="2" placeholder="Specific care instructions..."></textarea>
        </div>
      </div>

      <div class="gp-modal-footer">
        <button class="gp-btn gp-btn-secondary" ng-click="closeConfigModal()">Cancel</button>
        <button class="gp-btn gp-btn-save" ng-click="saveConfig()">Save & Sync Configuration</button>
      </div>
    </div>
  </div>

</div>

<!-- ================= EMBEDDED STYLES ================= -->
<style>
/* Reset & Full Screen Overrides */
html, body, md-content, .nr-dashboard-theme {{
  background-color: #070d18 !important;
  color: #f1f5f9 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Helvetica Neue", sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
  min-height: 100vh !important;
}}

/* Hide default retro toolbar to make dashboard 100% full screen */
md-toolbar.nr-dashboard-toolbar {{
  background: #0b1324 !important;
  border-bottom: 1px solid rgba(255,255,255,0.08) !important;
  height: 48px !important;
  min-height: 48px !important;
}}
.md-toolbar-tools {{
  height: 48px !important;
}}

/* Main Dashboard Wrapper */
.gp-dashboard {{
  padding: 16px 24px 40px 24px;
  max-width: 1600px;
  margin: 0 auto;
  box-sizing: border-box;
}}

/* Top Navigation Bar */
.gp-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  margin-bottom: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}}
.gp-brand {{
  display: flex;
  align-items: center;
  gap: 14px;
}}
.gp-logo-badge {{
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
}}
.gp-title {{
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.5px;
  color: #ffffff;
}}
.gp-accent {{
  color: #10b981;
}}
.gp-subtitle {{
  font-size: 11px;
  color: #94a3b8;
  font-weight: 500;
}}

.gp-header-center {{
  display: flex;
  gap: 10px;
  align-items: center;
}}
.gp-pill {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.06);
}}
.gp-pill-device {{
  background: rgba(30, 41, 59, 0.8);
  color: #cbd5e1;
}}
.gp-pill-aws {{
  background: rgba(6, 78, 59, 0.4);
  border-color: rgba(16, 185, 129, 0.3);
  color: #34d399;
}}
.gp-dot-live {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
}}
.pulse-emerald {{
  box-shadow: 0 0 10px #10b981;
  animation: pulseDot 2s infinite;
}}
@keyframes pulseDot {{
  0% {{ transform: scale(0.95); opacity: 0.8; }}
  50% {{ transform: scale(1.3); opacity: 1; }}
  100% {{ transform: scale(0.95); opacity: 0.8; }}
}}

.gp-header-actions {{
  display: flex;
  align-items: center;
  gap: 18px;
}}
.gp-clock {{
  text-align: right;
}}
.gp-clock-time {{
  font-size: 15px;
  font-weight: 700;
  color: #f8fafc;
  letter-spacing: 0.5px;
}}
.gp-clock-zone {{
  font-size: 10px;
  color: #64748b;
}}

.gp-btn {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 18px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}}
.gp-btn-config {{
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  color: #f1f5f9;
  border: 1px solid rgba(255, 255, 255, 0.12);
}}
.gp-btn-config:hover {{
  background: linear-gradient(135deg, #334155 0%, #475569 100%);
  border-color: #10b981;
  box-shadow: 0 0 14px rgba(16, 185, 129, 0.25);
}}

/* Active Plant & City Weather Banner */
.gp-meta-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}}
.gp-meta-card {{
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 18px 22px;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}}
.gp-plant-card {{
  border-left: 4px solid #10b981;
}}
.gp-weather-card {{
  border-left: 4px solid #06b6d4;
}}
.gp-meta-icon-box {{
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}
.gp-icon-emerald {{
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}}
.gp-icon-cyan {{
  background: rgba(6, 182, 212, 0.15);
  color: #06b6d4;
}}
.gp-icon-amber {{
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}}
.gp-icon-teal {{
  background: rgba(20, 184, 166, 0.15);
  color: #14b8a6;
}}
.gp-icon-blue {{
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}}
.gp-icon-purple {{
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}}
.gp-icon-sparkle {{
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 182, 212, 0.2) 100%);
  color: #34d399;
}}

.gp-meta-info {{
  flex: 1;
}}
.gp-meta-label {{
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #94a3b8;
  font-weight: 600;
  margin-bottom: 2px;
}}
.gp-meta-val-row {{
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}}
.gp-meta-title {{
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
}}
.gp-weather-cond {{
  font-size: 13px;
  color: #cbd5e1;
}}
.gp-badge {{
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}}
.gp-badge-emerald {{
  background: rgba(16, 185, 129, 0.18);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}}
.gp-meta-desc {{
  font-size: 12px;
  color: #64748b;
  margin-top: 3px;
}}
.gp-rain-status {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  margin-top: 4px;
}}
.rain-alert {{
  color: #38bdf8;
}}
.rain-clear {{
  color: #10b981;
}}
.gp-mini-btn {{
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.2s;
}}
.gp-mini-btn:hover {{
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
  border-color: #10b981;
}}

/* 6 Sensor Telemetry Cards Grid */
.gp-sensors-grid {{
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}}
@media (max-width: 1300px) {{
  .gp-sensors-grid {{ grid-template-columns: repeat(3, 1fr); }}
}}
@media (max-width: 768px) {{
  .gp-sensors-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .gp-meta-grid {{ grid-template-columns: 1fr; }}
  .gp-header {{ flex-direction: column; gap: 14px; align-items: flex-start; }}
}}

.gp-card {{
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 18px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
  transition: transform 0.2s, box-shadow 0.2s;
}}
.gp-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
}}

.gp-card-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}}
.gp-card-icon {{
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.gp-card-tag {{
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 3px 8px;
  border-radius: 6px;
}}
.tag-opt {{
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}}
.tag-warn {{
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
}}
.border-alert {{
  border-color: rgba(245, 158, 11, 0.5) !important;
}}
.border-optimal {{
  border-color: rgba(16, 185, 129, 0.3) !important;
}}

.gp-metric-val {{
  font-size: 32px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.5px;
  line-height: 1;
}}
.gp-unit {{
  font-size: 16px;
  color: #94a3b8;
  margin-left: 2px;
  font-weight: 600;
}}
.gp-metric-name {{
  font-size: 12px;
  color: #94a3b8;
  font-weight: 600;
  margin-top: 8px;
}}

.gp-bar-track {{
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  overflow: hidden;
  margin-top: 10px;
}}
.gp-bar-fill {{
  height: 100%;
  border-radius: 10px;
  transition: width 0.6s ease;
}}
.gp-fill-emerald {{ background: linear-gradient(90deg, #10b981, #34d399); }}
.gp-fill-teal {{ background: linear-gradient(90deg, #14b8a6, #2dd4bf); }}
.gp-fill-amber {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}
.gp-fill-blue {{ background: linear-gradient(90deg, #3b82f6, #60a5fa); }}
.gp-fill-cyan {{ background: linear-gradient(90deg, #06b6d4, #38bdf8); }}
.gp-fill-purple {{ background: linear-gradient(90deg, #a855f7, #c084fc); }}

.gp-range-hint {{
  font-size: 10px;
  color: #64748b;
  margin-top: 6px;
}}

/* Intelligence Grid (Health & AI Doctor) */
.gp-intelligence-grid {{
  display: grid;
  grid-template-columns: 1fr 1.6fr;
  gap: 20px;
  margin-bottom: 20px;
}}
@media (max-width: 1100px) {{
  .gp-intelligence-grid {{ grid-template-columns: 1fr; }}
}}

.gp-intel-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}}
.gp-intel-title-row {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.gp-intel-icon {{
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.gp-intel-title {{
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
}}
.gp-intel-sub {{
  font-size: 11px;
  color: #94a3b8;
}}

/* Physical Hardware LED Bar */
.gp-led-bar {{
  display: flex;
  justify-content: space-around;
  background: rgba(30, 41, 59, 0.6);
  padding: 14px 10px;
  border-radius: 12px;
  margin-bottom: 16px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}}
.gp-led-item {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  opacity: 0.35;
  transition: all 0.3s ease;
}}
.gp-led-bulb {{
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.2);
}}
.bulb-red {{ background: #ef4444; }}
.bulb-yellow {{ background: #f59e0b; }}
.bulb-green {{ background: #10b981; }}
.gp-led-label {{
  font-size: 10px;
  text-align: center;
  font-weight: 700;
  color: #94a3b8;
}}
.gp-led-label span {{
  font-size: 9px;
  font-weight: 400;
  color: #64748b;
}}
.active-red {{
  opacity: 1 !important;
}}
.active-red .bulb-red {{
  box-shadow: 0 0 16px #ef4444, 0 0 24px #ef4444;
}}
.active-yellow {{
  opacity: 1 !important;
}}
.active-yellow .bulb-yellow {{
  box-shadow: 0 0 16px #f59e0b, 0 0 24px #f59e0b;
}}
.active-green {{
  opacity: 1 !important;
}}
.active-green .bulb-green {{
  box-shadow: 0 0 16px #10b981, 0 0 24px #10b981;
}}

.gp-status-box {{
  padding: 14px 16px;
  border-radius: 12px;
  margin-bottom: 16px;
}}
.status-green {{
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.25);
  color: #34d399;
}}
.status-yellow {{
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.25);
  color: #fbbf24;
}}
.status-red {{
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: #f87171;
}}
.gp-status-head {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 4px;
}}
.gp-status-msg {{
  font-size: 12px;
  line-height: 1.4;
  color: #cbd5e1;
}}

/* Quick Test Sim Buttons */
.gp-sim-bar {{
  margin-top: 14px;
}}
.gp-sim-title {{
  font-size: 11px;
  color: #64748b;
  font-weight: 600;
  margin-bottom: 8px;
}}
.gp-sim-btns {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}}
.gp-btn-sim {{
  padding: 7px 8px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.04);
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.2s;
}}
.gp-btn-sim:hover {{
  background: rgba(255, 255, 255, 0.12);
  color: #ffffff;
}}

/* Gemini AI Card */
.gp-btn-ai-run {{
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: #ffffff;
  border: none;
  box-shadow: 0 0 16px rgba(16, 185, 129, 0.35);
}}
.gp-btn-ai-run:hover:not(:disabled) {{
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  box-shadow: 0 0 24px rgba(16, 185, 129, 0.6);
  transform: translateY(-1px);
}}
.gp-btn-ai-run:disabled {{
  opacity: 0.6;
  cursor: not-allowed;
}}
.gp-spin {{
  display: inline-block;
  animation: spin 1s linear infinite;
}}
@keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}

.gp-ai-content {{
  min-height: 180px;
  max-height: 380px;
  overflow-y: auto;
  padding: 14px 16px;
  background: rgba(11, 19, 36, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
}}
.gp-ai-loading-box {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 160px;
  gap: 14px;
}}
.gp-pulse-ring {{
  width: 38px;
  height: 38px;
  border: 3px solid rgba(16, 185, 129, 0.2);
  border-top-color: #10b981;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}}
.gp-loading-text {{
  font-size: 13px;
  color: #94a3b8;
  font-style: italic;
  text-align: center;
  max-width: 400px;
}}

.gp-ai-markdown {{
  font-size: 13px;
  line-height: 1.6;
  color: #e2e8f0;
}}
.gp-ai-markdown h3 {{
  color: #34d399;
  font-size: 14px;
  margin: 12px 0 6px 0;
  border-bottom: 1px solid rgba(16, 185, 129, 0.2);
  padding-bottom: 4px;
}}
.gp-ai-markdown ul {{
  margin: 6px 0 12px 18px;
  padding: 0;
}}
.gp-ai-markdown li {{
  margin-bottom: 4px;
}}
.gp-ai-markdown strong {{
  color: #ffffff;
}}

.gp-ai-footer {{
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  font-size: 11px;
  color: #64748b;
}}

/* Trends Chart Card */
.gp-chart-section {{
  margin-bottom: 20px;
}}
.gp-chart-card {{
  padding: 20px;
}}
.gp-chart-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}}
.gp-chart-title-row {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.gp-chart-legend {{
  display: flex;
  gap: 14px;
  font-size: 11px;
  color: #cbd5e1;
}}
.gp-legend-item {{
  display: flex;
  align-items: center;
  gap: 6px;
}}
.dot-emerald {{ width: 10px; height: 10px; border-radius: 50%; background: #10b981; }}
.dot-teal {{ width: 10px; height: 10px; border-radius: 50%; background: #14b8a6; }}
.dot-amber {{ width: 10px; height: 10px; border-radius: 50%; background: #f59e0b; }}
.dot-blue {{ width: 10px; height: 10px; border-radius: 50%; background: #3b82f6; }}
.gp-chart-canvas-wrap {{
  position: relative;
  width: 100%;
  height: 240px;
}}

/* Modal Backdrop & Dialog */
.gp-modal-backdrop {{
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(3, 7, 18, 0.82);
  backdrop-filter: blur(12px);
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}}
.gp-modal-content {{
  background: #0f172a;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
  max-width: 620px;
  width: 100%;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7);
  overflow: hidden;
  animation: modalIn 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}}
@keyframes modalIn {{
  from {{ transform: scale(0.92); opacity: 0; }}
  to {{ transform: scale(1); opacity: 1; }}
}}
.gp-modal-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  background: rgba(30, 41, 59, 0.4);
}}
.gp-modal-title-row {{
  display: flex;
  align-items: center;
  gap: 10px;
}}
.gp-modal-title-row h3 {{
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: #ffffff;
}}
.gp-modal-close {{
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
}}
.gp-modal-close:hover {{
  background: rgba(255,255,255,0.08);
  color: #ffffff;
}}

.gp-modal-body {{
  padding: 22px 24px;
}}
.gp-form-group {{
  margin-bottom: 16px;
}}
.gp-form-row {{
  display: flex;
  gap: 16px;
}}
.gp-col-6 {{
  flex: 1;
}}
.gp-form-label {{
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 6px;
}}
.gp-input {{
  width: 100%;
  padding: 10px 14px;
  border-radius: 10px;
  background: rgba(30, 41, 59, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #ffffff;
  font-size: 13px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
}}
.gp-input:focus {{
  border-color: #10b981;
  box-shadow: 0 0 10px rgba(16, 185, 129, 0.25);
}}
.gp-textarea {{
  resize: vertical;
}}

.gp-preset-chips {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}}
.gp-chip {{
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.2s;
}}
.gp-chip:hover {{
  background: rgba(16, 185, 129, 0.15);
  border-color: #10b981;
  color: #34d399;
}}
.chip-active {{
  background: #10b981 !important;
  color: #ffffff !important;
  border-color: #10b981 !important;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
}}

.gp-city-chips {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}}
.gp-chip-sm {{
  padding: 4px 10px;
  border-radius: 14px;
  font-size: 11px;
  font-weight: 600;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #94a3b8;
  cursor: pointer;
}}
.gp-chip-sm:hover {{
  color: #ffffff;
  border-color: #06b6d4;
}}

.gp-modal-footer {{
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  background: rgba(30, 41, 59, 0.4);
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}}
.gp-btn-secondary {{
  background: rgba(255, 255, 255, 0.08);
  color: #cbd5e1;
}}
.gp-btn-save {{
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: #ffffff;
  box-shadow: 0 0 16px rgba(16, 185, 129, 0.35);
}}
.gp-btn-save:hover {{
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  box-shadow: 0 0 24px rgba(16, 185, 129, 0.6);
}}
</style>

<!-- ================= EMBEDDED CONTROLLER ================= -->
<script>
(function(scope) {{

  scope.sensor = {{
    device_id: 'greenpulse-team-infinix',
    soil_moisture: 66.0,
    soil_temperature: 23.8,
    temperature: 25.2,
    humidity: 49.0,
    air_quality_percent: 100.0,
    air_pressure: 1012.1,
    timestamp: new Date().toISOString()
  }};

  scope.plant = {{
    plant_name: 'Tomato',
    location_name: 'Colombo',
    min_moisture: 50.0,
    max_moisture: 75.0,
    notes: 'High moisture requirement, regular watering needed'
  }};

  scope.weather = {{
    city: 'Colombo',
    temp: 26.9,
    humidity: 91,
    description: 'Overcast Clouds',
    rain_expected: true
  }};

  scope.presets = {{
    "Rose": {{"min_moisture": 30.0, "max_moisture": 70.0, "notes": "Moderate moisture, thrives in sunlight"}},
    "Tomato": {{"min_moisture": 50.0, "max_moisture": 75.0, "notes": "High moisture requirement, regular watering needed"}},
    "Monstera": {{"min_moisture": 35.0, "max_moisture": 65.0, "notes": "Allow top 2 inches to dry before watering"}},
    "Mint": {{"min_moisture": 55.0, "max_moisture": 75.0, "notes": "Loves moist soil, fast growing"}},
    "Cactus": {{"min_moisture": 10.0, "max_moisture": 30.0, "notes": "Drought tolerant, low water needs"}},
    "Succulent": {{"min_moisture": 15.0, "max_moisture": 35.0, "notes": "Allow soil to dry out between waterings"}},
    "Fern": {{"min_moisture": 60.0, "max_moisture": 80.0, "notes": "High humidity and consistently damp soil"}},
    "Chili / Pepper": {{"min_moisture": 45.0, "max_moisture": 70.0, "notes": "Warm conditions, steady moisture"}},
    "Orchid": {{"min_moisture": 25.0, "max_moisture": 50.0, "notes": "Epiphytic, needs well-draining medium"}}
  }};

  scope.quickCities = ["Colombo", "Kandy", "Galle", "Kurunegala", "Negombo", "Gampaha", "Nuwara Eliya", "Jaffna"];

  scope.statusLed = 'GREEN';
  scope.healthTitle = 'HEALTHY BOTANICAL CONDITION';
  scope.healthMessage = 'Soil moisture (66%) and microclimate metrics reside inside optimal boundaries for Tomato.';

  scope.aiLoading = false;
  scope.aiAdviceHtml = '<h3>Vital Signs Assessment</h3><p>Your tomato plant is thriving. Soil moisture is at <strong>66.0%</strong>, securely within the target safe band (50% – 75%).</p><h3>Weather & Irrigation Guidance</h3><p>Overcast clouds in <strong>Colombo</strong> with rain expected in the next 24 hours. <strong>Do not irrigate today</strong> to prevent root saturation.</p>';

  scope.currentTime = new Date().toLocaleTimeString();
  setInterval(function() {{
    scope.currentTime = new Date().toLocaleTimeString();
    scope.$applyAsync();
  }}, 1000);

  // Initialize
  scope.init = function() {{
    scope.fetchBackendConfig();
    scope.initChart();
  }};

  // Fetch initial config from port 5005
  scope.fetchBackendConfig = function() {{
    fetch('http://localhost:5005/api/config')
      .then(function(res) {{ return res.json(); }})
      .then(function(data) {{
        if (data && data.config) {{
          scope.plant = data.config;
          if (data.presets) scope.presets = data.presets;
          scope.refreshWeather();
          scope.evaluateStatus();
          scope.$applyAsync();
        }}
      }})
      .catch(function(err) {{
        console.warn('Backend API server not yet reached on 5005, using local state.');
      }});
  }};

  scope.refreshWeather = function() {{
    var city = scope.plant.location_name || 'Colombo';
    fetch('http://localhost:5005/api/weather?city=' + encodeURIComponent(city))
      .then(function(res) {{ return res.json(); }})
      .then(function(data) {{
        if (data) {{
          scope.weather = data;
          scope.evaluateStatus();
          scope.$applyAsync();
        }}
      }})
      .catch(function(e) {{}});
  }};

  // Modal handlers
  scope.showConfigModal = false;
  scope.tempConfig = {{}};

  scope.openConfigModal = function() {{
    scope.tempConfig = angular.copy(scope.plant);
    scope.showConfigModal = true;
  }};

  scope.closeConfigModal = function() {{
    scope.showConfigModal = false;
  }};

  scope.selectPreset = function(name, preset) {{
    scope.tempConfig.plant_name = name;
    scope.tempConfig.min_moisture = preset.min_moisture;
    scope.tempConfig.max_moisture = preset.max_moisture;
    scope.tempConfig.notes = preset.notes;
  }};

  scope.saveConfig = function() {{
    scope.plant = angular.copy(scope.tempConfig);
    scope.showConfigModal = false;

    fetch('http://localhost:5005/api/config', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(scope.plant)
    }})
    .then(function(res) {{ return res.json(); }})
    .then(function(data) {{
      if (data && data.weather) scope.weather = data.weather;
      scope.evaluateStatus();
      scope.runAiDiagnosis();
      scope.$applyAsync();
    }})
    .catch(function(err) {{
      scope.refreshWeather();
      scope.evaluateStatus();
    }});
  }};

  // Status Evaluation
  scope.evaluateStatus = function() {{
    var m = Number(scope.sensor.soil_moisture || 0);
    var t = Number(scope.sensor.temperature || 0);
    var minM = Number(scope.plant.min_moisture || 30);
    var maxM = Number(scope.plant.max_moisture || 70);

    if (m < minM) {{
      if (scope.weather.rain_expected) {{
        scope.statusLed = 'YELLOW';
        scope.healthTitle = 'WATER DEFICIT (RAIN APPROACHING)';
        scope.healthMessage = 'Soil moisture (' + m.toFixed(1) + '%) is low, but incoming rain in ' + scope.weather.city + ' will hydrate naturally. Monitor closely.';
      }} else {{
        scope.statusLed = 'RED';
        scope.healthTitle = 'WATERING NEEDED IMMEDIATELY';
        scope.healthMessage = 'Soil moisture (' + m.toFixed(1) + '%) dropped below minimum threshold (' + minM + '%). Irrigation required.';
      }}
    }} else if (t >= 33.0) {{
      scope.statusLed = 'RED';
      scope.healthTitle = 'HEAT STRESS WARNING';
      scope.healthMessage = 'Ambient temperature (' + t.toFixed(1) + '°C) exceeds safety limit. Provide shade or increase air circulation.';
    }} else if (m > maxM) {{
      scope.statusLed = 'YELLOW';
      scope.healthTitle = 'SOIL SATURATION WARNING';
      scope.healthMessage = 'Soil moisture (' + m.toFixed(1) + '%) is high. Hold all watering to protect root aeration.';
    }} else {{
      scope.statusLed = 'GREEN';
      scope.healthTitle = 'OPTIMAL HEALTH CONDITIONS';
      scope.healthMessage = 'All telemetry variables reside well within safe boundaries for ' + scope.plant.plant_name + '.';
    }}
  }};

  // Run AI Botanical Diagnosis
  scope.runAiDiagnosis = function() {{
    scope.aiLoading = true;

    fetch('http://localhost:5005/api/ai/diagnose', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{
        plant: scope.plant,
        sensor: scope.sensor
      }})
    }})
    .then(function(res) {{ return res.json(); }})
    .then(function(data) {{
      scope.aiLoading = false;
      if (data && data.advice) {{
        // Format markdown to HTML
        var html = data.advice
          .replace(/### (.*?)\\n/g, '<h3>$1</h3>')
          .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
          .replace(/\\* (.*?)\\n/g, '<li>$1</li>')
          .replace(/\\n\\n/g, '<br><br>');
        scope.aiAdviceHtml = html;
      }}
      scope.$applyAsync();
    }})
    .catch(function(err) {{
      scope.aiLoading = false;
      scope.aiAdviceHtml = '<h3>Offline Diagnostic Result</h3><p>' + scope.healthMessage + '</p>';
      scope.$applyAsync();
    }});
  }};

  // One-click Test Injections
  scope.injectTest = function(type) {{
    if (type === 'healthy') {{
      scope.sensor.soil_moisture = 65.0;
      scope.sensor.temperature = 25.0;
      scope.sensor.humidity = 55.0;
      scope.sensor.soil_temperature = 23.5;
    }} else if (type === 'dry') {{
      scope.sensor.soil_moisture = 22.0;
      scope.sensor.temperature = 28.5;
    }} else if (type === 'hot') {{
      scope.sensor.temperature = 34.5;
      scope.sensor.humidity = 40.0;
    }} else if (type === 'rain') {{
      scope.weather.rain_expected = true;
      scope.weather.description = 'Thunderstorms with Heavy Rain';
      scope.sensor.soil_moisture = 38.0;
    }}
    scope.evaluateStatus();
    scope.updateChartPoint();
    scope.$applyAsync();
  }};

  // Watch Node-RED incoming messages
  scope.$watch('msg', function(msg) {{
    if (!msg || !msg.payload) return;
    var p = msg.payload;

    if (p.temperature !== undefined) scope.sensor.temperature = Number(p.temperature);
    if (p.humidity !== undefined) scope.sensor.humidity = Number(p.humidity);
    if (p.soil_moisture !== undefined) scope.sensor.soil_moisture = Number(p.soil_moisture);
    if (p.soil_temperature !== undefined) scope.sensor.soil_temperature = Number(p.soil_temperature);
    if (p.air_quality_percent !== undefined) scope.sensor.air_quality_percent = Number(p.air_quality_percent);
    if (p.air_pressure !== undefined) scope.sensor.air_pressure = Number(p.air_pressure);
    if (p.device_id) scope.sensor.device_id = p.device_id;
    if (p.timestamp) scope.sensor.timestamp = p.timestamp;

    scope.evaluateStatus();
    scope.updateChartPoint();
    scope.$applyAsync();
  }});

  // Real-time Canvas Line Chart
  var chartHistory = {{
    labels: [],
    moisture: [],
    soilTemp: [],
    ambTemp: [],
    humidity: []
  }};

  scope.initChart = function() {{
    var now = new Date();
    for (var i = 10; i >= 0; i--) {{
      var t = new Date(now.getTime() - i * 5000);
      chartHistory.labels.push(t.toLocaleTimeString());
      chartHistory.moisture.push(scope.sensor.soil_moisture + (Math.random()*2 - 1));
      chartHistory.soilTemp.push(scope.sensor.soil_temperature + (Math.random()*0.4 - 0.2));
      chartHistory.ambTemp.push(scope.sensor.temperature + (Math.random()*0.4 - 0.2));
      chartHistory.humidity.push(scope.sensor.humidity + (Math.random()*2 - 1));
    }}
    scope.drawCanvasChart();
  }};

  scope.updateChartPoint = function() {{
    chartHistory.labels.push(new Date().toLocaleTimeString());
    chartHistory.moisture.push(scope.sensor.soil_moisture);
    chartHistory.soilTemp.push(scope.sensor.soil_temperature);
    chartHistory.ambTemp.push(scope.sensor.temperature);
    chartHistory.humidity.push(scope.sensor.humidity);

    if (chartHistory.labels.length > 25) {{
      chartHistory.labels.shift();
      chartHistory.moisture.shift();
      chartHistory.soilTemp.shift();
      chartHistory.ambTemp.shift();
      chartHistory.humidity.shift();
    }}
    scope.drawCanvasChart();
  }};

  scope.drawCanvasChart = function() {{
    var canvas = document.getElementById('gpTelemetryChart');
    if (!canvas) return;
    var ctx = canvas.getContext('2d');
    var w = canvas.width = canvas.parentElement.clientWidth;
    var h = canvas.height = 240;

    ctx.clearRect(0, 0, w, h);

    // Grid lines
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
    ctx.lineWidth = 1;
    for (var y = 20; y < h; y += 40) {{
      ctx.beginPath();
      ctx.moveTo(40, y);
      ctx.lineTo(w - 10, y);
      ctx.stroke();
    }}

    var pts = chartHistory.labels.length;
    if (pts < 2) return;
    var stepX = (w - 60) / (pts - 1);

    function plotLine(data, color, minV, maxV) {{
      ctx.strokeStyle = color;
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      for (var i = 0; i < pts; i++) {{
        var val = data[i];
        var normY = (val - minV) / (maxV - minV);
        if (normY < 0) normY = 0;
        if (normY > 1) normY = 1;
        var cx = 45 + i * stepX;
        var cy = h - 25 - normY * (h - 50);
        if (i === 0) ctx.moveTo(cx, cy);
        else ctx.lineTo(cx, cy);
      }}
      ctx.stroke();

      // Glowing dot at last point
      var lastX = 45 + (pts - 1) * stepX;
      var lastNorm = (data[pts - 1] - minV) / (maxV - minV);
      var lastY = h - 25 - lastNorm * (h - 50);
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(lastX, lastY, 4, 0, Math.PI * 2);
      ctx.fill();
    }}

    plotLine(chartHistory.moisture, '#10b981', 0, 100);
    plotLine(chartHistory.soilTemp, '#14b8a6', 10, 40);
    plotLine(chartHistory.ambTemp, '#f59e0b', 10, 45);
    plotLine(chartHistory.humidity, '#3b82f6', 0, 100);
  }};

  window.addEventListener('resize', function() {{
    scope.drawCanvasChart();
  }});

}})(scope);
</script>
"""

# Construct Node-RED Flow
flow = [
    {
        "id": "tab_greenpulse",
        "type": "tab",
        "label": "GreenPulse Live Monitor",
        "disabled": False,
        "info": "GreenPulse Autonomous Botanical Intelligence & Telemetry Dashboard"
    },
    {
        "id": "ui_tab_main",
        "type": "ui_tab",
        "name": "Live Monitor",
        "icon": "dashboard",
        "order": 1
    },
    {
        "id": "ui_group_main",
        "type": "ui_group",
        "name": "Live Botanical Telemetry",
        "tab": "ui_tab_main",
        "order": 1,
        "disp": False,
        "width": "12",
        "collapse": False
    },
    {
        "id": "http_sensor_in",
        "type": "http in",
        "z": "tab_greenpulse",
        "name": "POST /api/sensor",
        "url": "/api/sensor",
        "method": "post",
        "upload": False,
        "swaggerDoc": "",
        "x": 140,
        "y": 100,
        "wires": [["http_sensor_out", "fn_parse_telemetry"]]
    },
    {
        "id": "http_sensor_out",
        "type": "http response",
        "z": "tab_greenpulse",
        "name": "200 OK",
        "statusCode": "200",
        "headers": {"Content-Type": "application/json"},
        "x": 360,
        "y": 60,
        "wires": []
    },
    {
        "id": "fn_parse_telemetry",
        "type": "function",
        "z": "tab_greenpulse",
        "name": "Format Telemetry Msg",
        "func": """var data = msg.payload || {};
return {
    payload: {
        device_id: data.device_id || 'greenpulse-team-infinix',
        temperature: Number(data.temperature || 25.2),
        humidity: Number(data.humidity || 49.0),
        soil_moisture: Number(data.soil_moisture || 66.0),
        soil_temperature: Number(data.soil_temperature || 23.8),
        air_quality_percent: Number(data.air_quality_percent || 100.0),
        air_pressure: Number(data.air_pressure || 1012.1),
        timestamp: data.timestamp || new Date().toISOString()
    }
};""",
        "outputs": 1,
        "noerr": 0,
        "x": 420,
        "y": 120,
        "wires": [["ui_full_template"]]
    },
    {
        "id": "inject_healthy",
        "type": "inject",
        "z": "tab_greenpulse",
        "name": "Healthy Tomato (Colombo)",
        "props": [
            {
                "p": "payload",
                "v": '{"device_id":"greenpulse-team-infinix","soil_moisture":66.0,"temperature":25.2,"humidity":49.0,"soil_temperature":23.8,"air_quality_percent":100.0,"air_pressure":1012.1}',
                "vt": "json"
            }
        ],
        "repeat": "",
        "crontab": "",
        "once": False,
        "onceDelay": 0.1,
        "topic": "",
        "x": 170,
        "y": 180,
        "wires": [["fn_parse_telemetry"]]
    },
    {
        "id": "inject_dry",
        "type": "inject",
        "z": "tab_greenpulse",
        "name": "Dry Soil Deficit (22%)",
        "props": [
            {
                "p": "payload",
                "v": '{"device_id":"greenpulse-team-infinix","soil_moisture":22.0,"temperature":29.0,"humidity":42.0,"soil_temperature":25.0,"air_quality_percent":98.0,"air_pressure":1011.5}',
                "vt": "json"
            }
        ],
        "repeat": "",
        "crontab": "",
        "once": False,
        "onceDelay": 0.1,
        "topic": "",
        "x": 160,
        "y": 240,
        "wires": [["fn_parse_telemetry"]]
    },
    {
        "id": "inject_heat",
        "type": "inject",
        "z": "tab_greenpulse",
        "name": "Heat Stress Warning (34.5°C)",
        "props": [
            {
                "p": "payload",
                "v": '{"device_id":"greenpulse-team-infinix","soil_moisture":42.0,"temperature":34.5,"humidity":38.0,"soil_temperature":28.5,"air_quality_percent":95.0,"air_pressure":1010.2}',
                "vt": "json"
            }
        ],
        "repeat": "",
        "crontab": "",
        "once": False,
        "onceDelay": 0.1,
        "topic": "",
        "x": 180,
        "y": 300,
        "wires": [["fn_parse_telemetry"]]
    },
    {
        "id": "ui_full_template",
        "type": "ui_template",
        "z": "tab_greenpulse",
        "group": "ui_group_main",
        "name": "Full-Screen GreenPulse Luxury UI",
        "order": 1,
        "width": "12",
        "height": "28",
        "format": TEMPLATE_HTML,
        "storeOutMessages": True,
        "fwdInMessages": True,
        "resendOnRefresh": True,
        "templateScope": "local",
        "className": "",
        "x": 740,
        "y": 140,
        "wires": [[]]
    }
]

def main():
    json_str = json.dumps(flow, indent=4)
    with open(FLOW_FILE, "w", encoding="utf-8") as f:
        f.write(json_str)
    print(f"Saved {len(flow)} nodes to {FLOW_FILE}")

    # Deploy flow to Node-RED directly via API
    try:
        resp = requests.post(
            "http://localhost:1880/flows",
            headers={"Content-Type": "application/json", "Node-RED-Deployment-Type": "full"},
            data=json_str,
            timeout=5
        )
        print(f"Node-RED API Deploy Status: {resp.status_code}")
    except Exception as e:
        print(f"Deploy via API: {e}")

if __name__ == "__main__":
    main()
