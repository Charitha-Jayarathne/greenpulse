"""
Build Full-Screen Light-Theme Node-RED Flow for GreenPulse
"""

import json
from pathlib import Path
import requests

FLOW_FILE = Path("f:/greenpulse/node_red_flow.json")

# Crisp React / Lucide SVG Icons
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

SVG_CLOUD = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>"""

LIGHT_TEMPLATE_HTML = f"""
<div id="gp-app" class="gp-dashboard" ng-init="init()">

  <!-- ================= TOP HEADER ================= -->
  <header class="gp-header">
    <div class="gp-brand">
      <div class="gp-logo-badge">
        {SVG_SPROUT}
      </div>
      <div>
        <div class="gp-title">GreenPulse <span class="gp-accent">IoT Core</span></div>
        <div class="gp-subtitle">Autonomous Botanical Intelligence & Plant Care</div>
      </div>
    </div>

    <div class="gp-header-center">
      <div class="gp-pill gp-pill-device">
        <span class="gp-dot-live"></span>
        <span>ESP32: <strong>{{{{sensor.device_id || 'greenpulse-team-infinix'}}}}</strong></span>
      </div>
      <div class="gp-pill gp-pill-aws">
        <span class="gp-dot-live pulse-emerald"></span>
        <span>AWS IoT Core mTLS (Port 8883) CONNECTED</span>
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
          <span class="gp-badge gp-badge-emerald">Safe Moisture: {{{{plant.min_moisture}}}}% – {{{{plant.max_moisture}}}}%</span>
        </div>
        <div class="gp-meta-desc">{{{{plant.notes || 'Target botanical parameters actively guarded'}}}}</div>
      </div>
      <button class="gp-btn-switch" ng-click="openConfigModal()">
        {SVG_SETTINGS}
        <span>Change</span>
      </button>
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
          <span ng-if="weather.rain_expected">{SVG_RAIN} Rain Expected within 24h — Automated Irrigation Delay Advised</span>
          <span ng-if="!weather.rain_expected">{SVG_SUN} Clear Weather Forecast — Regular Irrigation Schedule Active</span>
        </div>
      </div>
      <button class="gp-btn-switch" ng-click="refreshWeather()">
        {SVG_REFRESH}
        <span>Refresh</span>
      </button>
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
      <div class="gp-range-hint">Safe Target: {{{{plant.min_moisture}}}}% – {{{{plant.max_moisture}}}}%</div>
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
      <div class="gp-range-hint">Root Comfort: 18.0°C – 28.0°C</div>
    </div>

    <!-- 3. Ambient Temperature (DHT22) -->
    <div class="gp-card gp-card-metric">
      <div class="gp-card-header">
        <span class="gp-card-icon gp-icon-amber">{SVG_THERMO}</span>
        <span class="gp-card-tag" ng-class="{{'tag-opt': sensor.temperature <= 32, 'tag-warn': sensor.temperature > 32}}">
          {{{{sensor.temperature <= 32 ? 'Optimal Thermal' : 'Heat Warning'}}}}
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
        <span class="gp-card-icon gp-icon-blue">{SVG_CLOUD}</span>
        <span class="gp-card-tag tag-opt">Air Moisture</span>
      </div>
      <div class="gp-metric-val">{{{{sensor.humidity | number:1}}}}<span class="gp-unit">%</span></div>
      <div class="gp-metric-name">Relative Humidity (DHT22)</div>
      <div class="gp-bar-track">
        <div class="gp-bar-fill gp-fill-blue" style="width: {{{{sensor.humidity}}}}%;"></div>
      </div>
      <div class="gp-range-hint">Normal Transpiration: 40% – 70%</div>
    </div>

    <!-- 5. Air Quality MQ Sensor -->
    <div class="gp-card gp-card-metric">
      <div class="gp-card-header">
        <span class="gp-card-icon gp-icon-cyan">{SVG_WIND}</span>
        <span class="gp-card-tag tag-opt">Gas & Purity</span>
      </div>
      <div class="gp-metric-val">{{{{sensor.air_quality_percent | number:0}}}}<span class="gp-unit">%</span></div>
      <div class="gp-metric-name">Air Quality Level (MQ)</div>
      <div class="gp-bar-track">
        <div class="gp-bar-fill gp-fill-cyan" style="width: {{{{sensor.air_quality_percent}}}}%;"></div>
      </div>
      <div class="gp-range-hint">Purity Status: Pure & Clean Air</div>
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

  <!-- ================= TELEMETRY TRENDS & AI DOCTOR ROW ================= -->
  <section class="gp-intelligence-grid">
    <!-- Multi-Sensor Telemetry Trends Line Graph Card (Replaces LED Card) -->
    <div class="gp-card gp-chart-card">
      <div class="gp-chart-header">
        <div class="gp-chart-title-row">
          <span class="gp-intel-icon gp-icon-teal">{SVG_ACTIVITY}</span>
          <div>
            <div class="gp-intel-title">Multi-Sensor Telemetry Trends</div>
            <div class="gp-intel-sub">Live 60-Second Real-time Sensor Stream</div>
          </div>
        </div>

        <div class="gp-chart-legend">
          <span class="gp-legend-item"><span class="dot-emerald"></span> Moisture</span>
          <span class="gp-legend-item"><span class="dot-teal"></span> Soil T</span>
          <span class="gp-legend-item"><span class="dot-amber"></span> Amb T</span>
          <span class="gp-legend-item"><span class="dot-blue"></span> Humidity</span>
        </div>
      </div>

      <div class="gp-chart-canvas-wrap">
        <canvas id="gpTelemetryChart" height="260"></canvas>
      </div>

      <!-- Quick Demonstration Scenarios Bar -->
      <div class="gp-sim-bar">
        <div class="gp-sim-title">One-Click Demonstration Scenarios:</div>
        <div class="gp-sim-btns">
          <button class="gp-btn-sim sim-opt" ng-click="injectTest('healthy')">Healthy Plant</button>
          <button class="gp-btn-sim sim-dry" ng-click="injectTest('dry')">Dry Soil Alert</button>
          <button class="gp-btn-sim sim-hot" ng-click="injectTest('hot')">Heat Stress</button>
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
          <div class="gp-loading-text">Synthesizing real-time telemetry, soil moisture, and {{{{weather.city}}}} forecast with Gemini 3.8 Flash...</div>
        </div>

        <div ng-if="!aiLoading" class="gp-ai-markdown" ng-bind-html="aiAdviceHtml"></div>
      </div>

      <div class="gp-ai-footer">
        <span>Model: Google Gemini 3.8 Flash</span>
        <span>Decision Engine: Synchronized</span>
        <span>Physical Telemetry: Live</span>
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

<!-- ================= MODERN LIGHT THEME FULL SCREEN STYLES ================= -->
<style>
/* 1. Force Full Screen 100% Width & Break Out of Node-RED Grid */
html, body, md-content, .nr-dashboard-theme {{
  background-color: #f8fafc !important;
  color: #0f172a !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  overflow: hidden !important;
}}

/* Hide default Node-RED blue toolbar so our luxury header takes full top space */
md-toolbar.nr-dashboard-toolbar {{
  display: none !important;
}}

/* TRUE FULL-SCREEN ROOT CONTAINER (Takes 100% viewport width and height) */
#gp-app.gp-dashboard {{
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  max-width: 100vw !important;
  max-height: 100vh !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  z-index: 9999 !important;
  background-color: #f8fafc !important;
  box-sizing: border-box !important;
  padding: 24px 36px 60px 36px !important;
}}

/* Top Navigation Bar */
.gp-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  margin-bottom: 24px;
  box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
}}
.gp-brand {{
  display: flex;
  align-items: center;
  gap: 14px;
}}
.gp-logo-badge {{
  width: 46px;
  height: 46px;
  border-radius: 12px;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
}}
.gp-title {{
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: #0f172a;
}}
.gp-accent {{
  color: #059669;
}}
.gp-subtitle {{
  font-size: 12px;
  color: #64748b;
  font-weight: 500;
}}

.gp-header-center {{
  display: flex;
  gap: 12px;
  align-items: center;
}}
.gp-pill {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 16px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 600;
}}
.gp-pill-device {{
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #334155;
}}
.gp-pill-aws {{
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  color: #047857;
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
  0% {{ transform: scale(0.9); opacity: 0.8; }}
  50% {{ transform: scale(1.3); opacity: 1; }}
  100% {{ transform: scale(0.9); opacity: 0.8; }}
}}

.gp-header-actions {{
  display: flex;
  align-items: center;
  gap: 20px;
}}
.gp-clock {{
  text-align: right;
}}
.gp-clock-time {{
  font-size: 16px;
  font-weight: 700;
  color: #0f172a;
  letter-spacing: 0.5px;
}}
.gp-clock-zone {{
  font-size: 11px;
  color: #64748b;
}}

.gp-btn {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}}
.gp-btn-config {{
  background: #0f172a;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}}
.gp-btn-config:hover {{
  background: #059669;
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.25);
  transform: translateY(-1px);
}}

/* Active Plant & City Weather Banner */
.gp-meta-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}}
.gp-meta-card {{
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 20px 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}}
.gp-plant-card {{
  border-left: 5px solid #10b981;
}}
.gp-weather-card {{
  border-left: 5px solid #06b6d4;
}}
.gp-meta-icon-box {{
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}
.gp-icon-emerald {{
  background: #ecfdf5;
  color: #059669;
}}
.gp-icon-cyan {{
  background: #ecfeff;
  color: #0891b2;
}}
.gp-icon-amber {{
  background: #fffbeb;
  color: #d97706;
}}
.gp-icon-teal {{
  background: #f0fdfa;
  color: #0d9488;
}}
.gp-icon-blue {{
  background: #eff6ff;
  color: #2563eb;
}}
.gp-icon-purple {{
  background: #f5f3ff;
  color: #7c3aed;
}}
.gp-icon-sparkle {{
  background: linear-gradient(135deg, #ecfdf5 0%, #ecfeff 100%);
  color: #059669;
}}

.gp-meta-info {{
  flex: 1;
}}
.gp-meta-label {{
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #64748b;
  font-weight: 700;
  margin-bottom: 3px;
}}
.gp-meta-val-row {{
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}}
.gp-meta-title {{
  font-size: 20px;
  font-weight: 800;
  color: #0f172a;
}}
.gp-weather-cond {{
  font-size: 13px;
  color: #334155;
  font-weight: 600;
}}
.gp-badge {{
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 700;
}}
.gp-badge-emerald {{
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}}
.gp-meta-desc {{
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}}
.gp-rain-status {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 600;
  margin-top: 6px;
}}
.rain-alert {{
  color: #0284c7;
}}
.rain-clear {{
  color: #059669;
}}
.gp-btn-switch {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 700;
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s;
}}
.gp-btn-switch:hover {{
  background: #059669;
  color: #ffffff;
  border-color: #059669;
}}

/* 6 Sensor Telemetry Cards Grid - Full Width Responsive */
.gp-sensors-grid {{
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}}
@media (max-width: 1400px) {{
  .gp-sensors-grid {{ grid-template-columns: repeat(3, 1fr); }}
}}
@media (max-width: 800px) {{
  .gp-sensors-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .gp-meta-grid {{ grid-template-columns: 1fr; }}
  .gp-header {{ flex-direction: column; gap: 16px; align-items: flex-start; }}
}}

.gp-card {{
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
  transition: transform 0.2s, box-shadow 0.2s;
}}
.gp-card:hover {{
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}}

.gp-card-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}}
.gp-card-icon {{
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.gp-card-tag {{
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 6px;
}}
.tag-opt {{
  background: #ecfdf5;
  color: #047857;
  border: 1px solid #a7f3d0;
}}
.tag-warn {{
  background: #fffbeb;
  color: #b45309;
  border: 1px solid #fde68a;
}}
.border-alert {{
  border-color: #f59e0b !important;
}}
.border-optimal {{
  border-color: #10b981 !important;
}}

.gp-metric-val {{
  font-size: 34px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.5px;
  line-height: 1;
}}
.gp-unit {{
  font-size: 16px;
  color: #64748b;
  margin-left: 3px;
  font-weight: 600;
}}
.gp-metric-name {{
  font-size: 12px;
  color: #475569;
  font-weight: 700;
  margin-top: 10px;
}}

.gp-bar-track {{
  width: 100%;
  height: 7px;
  background: #f1f5f9;
  border-radius: 10px;
  overflow: hidden;
  margin-top: 10px;
}}
.gp-bar-fill {{
  height: 100%;
  border-radius: 10px;
  transition: width 0.6s ease;
}}
.gp-fill-emerald {{ background: linear-gradient(90deg, #10b981, #059669); }}
.gp-fill-teal {{ background: linear-gradient(90deg, #14b8a6, #0d9488); }}
.gp-fill-amber {{ background: linear-gradient(90deg, #f59e0b, #d97706); }}
.gp-fill-blue {{ background: linear-gradient(90deg, #3b82f6, #2563eb); }}
.gp-fill-cyan {{ background: linear-gradient(90deg, #06b6d4, #0891b2); }}
.gp-fill-purple {{ background: linear-gradient(90deg, #8b5cf6, #7c3aed); }}

.gp-range-hint {{
  font-size: 10px;
  color: #94a3b8;
  font-weight: 500;
  margin-top: 8px;
}}

/* Intelligence Grid (Health & AI Doctor) */
.gp-intelligence-grid {{
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}}
@media (max-width: 1100px) {{
  .gp-intelligence-grid {{ grid-template-columns: 1fr; }}
}}

.gp-intel-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  padding-bottom: 14px;
  border-bottom: 1px solid #f1f5f9;
}}
.gp-intel-title-row {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.gp-intel-icon {{
  width: 42px;
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.gp-intel-title {{
  font-size: 17px;
  font-weight: 800;
  color: #0f172a;
}}
.gp-intel-sub {{
  font-size: 12px;
  color: #64748b;
}}

/* Physical Hardware LED Bar (Dark Housing on Light Card for High Contrast) */
.gp-led-bar {{
  display: flex;
  justify-content: space-around;
  background: #0f172a;
  padding: 16px 14px;
  border-radius: 14px;
  margin-bottom: 18px;
  box-shadow: inset 0 2px 6px rgba(0, 0, 0, 0.4);
}}
.gp-led-item {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  opacity: 0.35;
  transition: all 0.3s ease;
}}
.gp-led-bulb {{
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.25);
}}
.bulb-red {{ background: #ef4444; }}
.bulb-yellow {{ background: #f59e0b; }}
.bulb-green {{ background: #10b981; }}
.gp-led-label {{
  font-size: 11px;
  text-align: center;
  font-weight: 700;
  color: #cbd5e1;
}}
.gp-led-label span {{
  font-size: 9px;
  font-weight: 400;
  color: #94a3b8;
}}
.active-red {{
  opacity: 1 !important;
}}
.active-red .bulb-red {{
  box-shadow: 0 0 16px #ef4444, 0 0 28px #ef4444;
}}
.active-yellow {{
  opacity: 1 !important;
}}
.active-yellow .bulb-yellow {{
  box-shadow: 0 0 16px #f59e0b, 0 0 28px #f59e0b;
}}
.active-green {{
  opacity: 1 !important;
}}
.active-green .bulb-green {{
  box-shadow: 0 0 16px #10b981, 0 0 28px #10b981;
}}

.gp-status-box {{
  padding: 16px 18px;
  border-radius: 12px;
  margin-bottom: 18px;
}}
.status-green {{
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
  color: #047857;
}}
.status-yellow {{
  background: #fffbeb;
  border: 1px solid #fde68a;
  color: #b45309;
}}
.status-red {{
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}}
.gp-status-head {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 800;
  margin-bottom: 4px;
}}
.gp-status-msg {{
  font-size: 13px;
  line-height: 1.5;
  color: #334155;
}}

/* Quick Test Sim Buttons */
.gp-sim-bar {{
  margin-top: 14px;
}}
.gp-sim-title {{
  font-size: 11px;
  color: #64748b;
  font-weight: 700;
  margin-bottom: 8px;
  text-transform: uppercase;
}}
.gp-sim-btns {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 8px;
}}
.gp-btn-sim {{
  padding: 8px 10px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  border: 1px solid #cbd5e1;
  background: #f8fafc;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s;
}}
.gp-btn-sim:hover {{
  background: #0f172a;
  color: #ffffff;
  border-color: #0f172a;
}}

/* Gemini AI Card (Light Theme) */
.gp-btn-ai-run {{
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: #ffffff;
  border: none;
  box-shadow: 0 4px 14px rgba(5, 150, 105, 0.3);
}}
.gp-btn-ai-run:hover:not(:disabled) {{
  background: linear-gradient(135deg, #047857 0%, #059669 100%);
  box-shadow: 0 6px 20px rgba(5, 150, 105, 0.45);
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
  min-height: 200px;
  max-height: 380px;
  overflow-y: auto;
  padding: 18px 20px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}}
.gp-ai-loading-box {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 180px;
  gap: 16px;
}}
.gp-pulse-ring {{
  width: 42px;
  height: 42px;
  border: 4px solid #d1fae5;
  border-top-color: #059669;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}}
.gp-loading-text {{
  font-size: 13px;
  color: #64748b;
  font-style: italic;
  text-align: center;
  max-width: 420px;
}}

.gp-ai-markdown {{
  font-size: 13px;
  line-height: 1.7;
  color: #1e293b;
}}
.gp-ai-markdown h3 {{
  color: #047857;
  font-size: 15px;
  font-weight: 800;
  margin: 14px 0 6px 0;
  border-bottom: 2px solid #a7f3d0;
  padding-bottom: 4px;
}}
.gp-ai-markdown ul {{
  margin: 6px 0 12px 20px;
  padding: 0;
}}
.gp-ai-markdown li {{
  margin-bottom: 5px;
}}
.gp-ai-markdown strong {{
  color: #0f172a;
}}

.gp-ai-footer {{
  display: flex;
  justify-content: space-between;
  margin-top: 14px;
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
}}

/* Trends Chart Card */
.gp-chart-section {{
  margin-bottom: 24px;
}}
.gp-chart-card {{
  padding: 24px;
}}
.gp-chart-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
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
  gap: 16px;
  font-size: 12px;
  color: #334155;
  font-weight: 600;
}}
.gp-legend-item {{
  display: flex;
  align-items: center;
  gap: 6px;
}}
.dot-emerald {{ width: 10px; height: 10px; border-radius: 50%; background: #059669; }}
.dot-teal {{ width: 10px; height: 10px; border-radius: 50%; background: #0d9488; }}
.dot-amber {{ width: 10px; height: 10px; border-radius: 50%; background: #d97706; }}
.dot-blue {{ width: 10px; height: 10px; border-radius: 50%; background: #2563eb; }}
.gp-chart-canvas-wrap {{
  position: relative;
  width: 100%;
  height: 240px;
}}

/* Modal Backdrop & Dialog (Clean Light Styling) */
.gp-modal-backdrop {{
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(8px);
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  box-sizing: border-box;
}}
.gp-modal-content {{
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  max-width: 620px;
  width: 100%;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.25);
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
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
}}
.gp-modal-title-row {{
  display: flex;
  align-items: center;
  gap: 10px;
}}
.gp-modal-title-row h3 {{
  margin: 0;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}}
.gp-modal-close {{
  background: none;
  border: none;
  color: #64748b;
  font-size: 18px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
}}
.gp-modal-close:hover {{
  background: #e2e8f0;
  color: #0f172a;
}}

.gp-modal-body {{
  padding: 24px;
}}
.gp-form-group {{
  margin-bottom: 18px;
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
  font-weight: 700;
  color: #475569;
  margin-bottom: 6px;
}}
.gp-input {{
  width: 100%;
  padding: 11px 14px;
  border-radius: 10px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  color: #0f172a;
  font-size: 13px;
  box-sizing: border-box;
  outline: none;
  transition: border-color 0.2s;
}}
.gp-input:focus {{
  border-color: #059669;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.15);
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
  padding: 7px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s;
}}
.gp-chip:hover {{
  background: #ecfdf5;
  border-color: #059669;
  color: #059669;
}}
.chip-active {{
  background: #059669 !important;
  color: #ffffff !important;
  border-color: #059669 !important;
  box-shadow: 0 4px 10px rgba(5, 150, 105, 0.35);
}}

.gp-city-chips {{
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}}
.gp-chip-sm {{
  padding: 5px 12px;
  border-radius: 14px;
  font-size: 11px;
  font-weight: 600;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #475569;
  cursor: pointer;
}}
.gp-chip-sm:hover {{
  color: #0284c7;
  border-color: #38bdf8;
  background: #f0f9ff;
}}

.gp-modal-footer {{
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}}
.gp-btn-secondary {{
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
}}
.gp-btn-save {{
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(5, 150, 105, 0.35);
}}
.gp-btn-save:hover {{
  background: linear-gradient(135deg, #047857 0%, #059669 100%);
  box-shadow: 0 6px 20px rgba(5, 150, 105, 0.45);
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

  // Real-time Canvas Line Chart (Light theme grid & lines)
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

    // Light Theme Grid lines
    ctx.strokeStyle = '#e2e8f0';
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

      var lastX = 45 + (pts - 1) * stepX;
      var lastNorm = (data[pts - 1] - minV) / (maxV - minV);
      var lastY = h - 25 - lastNorm * (h - 50);
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(lastX, lastY, 4, 0, Math.PI * 2);
      ctx.fill();
    }}

    plotLine(chartHistory.moisture, '#059669', 0, 100);
    plotLine(chartHistory.soilTemp, '#0d9488', 10, 40);
    plotLine(chartHistory.ambTemp, '#d97706', 10, 45);
    plotLine(chartHistory.humidity, '#2563eb', 0, 100);
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
        "info": "GreenPulse Full-Screen Light Theme Botanical Intelligence & Telemetry Dashboard"
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
        "width": "24",
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
        "name": "Full-Screen GreenPulse Light UI",
        "order": 1,
        "width": "24",
        "height": "28",
        "format": LIGHT_TEMPLATE_HTML,
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
