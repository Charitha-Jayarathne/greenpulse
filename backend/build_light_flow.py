import json
from pathlib import Path
import requests

FLOW_FILE = Path(__file__).resolve().parent.parent / "node_red_flow.json"
BUILD_SCRIPT = Path(__file__).resolve()

# Icons
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
SVG_ALERT = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>"""
SVG_REFRESH = """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>"""
SVG_SUN = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>"""
SVG_CLOUD = """<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/></svg>"""
SVG_SATELLITE = """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 7 9 3 5 7l4 4"/><path d="m17 11 4 4-4 4-4-4"/><path d="m8 12 4 4"/><path d="m16 8-4-4"/><path d="M12 12v.01"/></svg>"""
SVG_SHUFFLE = """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18h1.4c1.3 0 2.5-.6 3.3-1.7l6.1-8.6c.8-1.1 2-1.7 3.3-1.7H22"/><path d="m18 2 4 4-4 4"/><path d="M2 6h1.4c1.3 0 2.5.6 3.3 1.7l6.1 8.6c.8 1.1 2 1.7 3.3 1.7H22"/><path d="m18 14 4 4-4 4"/></svg>"""

TEMPLATE_HTML = f"""
<div id="gp-app" class="gp-dashboard" ng-init="init()">

  <!-- ======================================================== -->
  <!-- VIEW 1: PLANT REGISTRATION & BOTANICAL ONBOARDING SCREEN -->
  <!-- ======================================================== -->
  <div class="gp-reg-container" ng-show="viewMode === 'register'">
    <div class="gp-reg-card">
      
      <!-- Registration Header -->
      <div class="gp-reg-header">
        <div class="gp-brand">
          <div class="gp-logo-badge">
            {SVG_SPROUT}
          </div>
          <div>
            <div class="gp-title">GreenPulse <span class="gp-accent">IoT Hub</span></div>
            <div class="gp-subtitle">Botanical Node Pairing & Plant Registration</div>
          </div>
        </div>

        <div class="gp-pill gp-pill-device">
          <span class="gp-dot-live pulse-emerald"></span>
          <span>ESP32 Node: <strong>{{{{activeDeviceId}}}}</strong></span>
        </div>
      </div>

      <!-- Registration Steps Form -->
      <form class="gp-reg-form" ng-submit="submitRegistration()">
        
        <!-- Step 1: AI Plant Identification & Autonomous Calibration -->
        <div class="gp-form-section">
          <div class="gp-section-title">
            <span class="gp-step-num">1</span>
            <span>Identify Plant via Gemini 3.8 Flash AI:</span>
          </div>
          
          <div class="gp-search-box-wrap">
            <div class="gp-search-input-row">
              <input type="text" 
                     class="gp-input gp-input-search" 
                     ng-model="plantSearchQuery" 
                     placeholder="Type plant name or species (e.g. Snake Plant, Karapincha, Tomato, Aloe Vera...)"
                     ng-keydown="$event.keyCode === 13 && ($event.preventDefault(), searchAndIdentifyPlant())">
              <button type="button" 
                      class="gp-btn gp-btn-ai-search" 
                      ng-click="searchAndIdentifyPlant()" 
                      ng-disabled="aiSearching || !plantSearchQuery">
                <span ng-if="!aiSearching">{SVG_SPARKLES}</span>
                <span ng-if="aiSearching" class="gp-spin">{SVG_REFRESH}</span>
                <span>{{{{aiSearching ? 'AI Consulting...' : '✨ AI Identify & Calibrate'}}}}</span>
              </button>
            </div>

            <!-- Quick Suggestions Tags -->
            <div class="gp-quick-search-tags">
              <span class="gp-quick-label">💡 Botanical Suggestions:</span>
              <button type="button" class="gp-tag-chip" ng-click="quickSelectPlant('Snake Plant')">🌱 Snake Plant</button>
              <button type="button" class="gp-tag-chip" ng-click="quickSelectPlant('Karapincha / Curry Leaves')">🌿 Curry Leaves (Karapincha)</button>
              <button type="button" class="gp-tag-chip" ng-click="quickSelectPlant('Tomato')">🍅 Tomato</button>
              <button type="button" class="gp-tag-chip" ng-click="quickSelectPlant('Monstera Deliciosa')">🍃 Monstera</button>
              <button type="button" class="gp-tag-chip" ng-click="quickSelectPlant('Aloe Vera')">🌵 Aloe Vera</button>
              <button type="button" class="gp-tag-chip" ng-click="quickSelectPlant('Chili / Pepper')">🌶️ Chili / Pepper</button>
              <button type="button" class="gp-tag-chip" ng-click="quickSelectPlant('Mint')">🌱 Mint</button>
              <button type="button" class="gp-tag-chip" ng-click="quickSelectPlant('Orchid')">🌸 Orchid</button>
            </div>
          </div>

          <!-- AI Loading Animation -->
          <div class="gp-ai-identifying-banner" ng-if="aiSearching">
            <div class="gp-spin-glow">{SVG_SPARKLES}</div>
            <div>
              <strong>Gemini 3.8 Flash Botanical Model in progress...</strong>
              <div class="gp-sub-txt">Consulting taxonomic databases and calculating precise root-zone volumetric moisture boundaries for "{{{{plantSearchQuery}}}}"...</div>
            </div>
          </div>

          <!-- AI Botanical Profile Card (Populated by Gemini AI) -->
          <div class="gp-ai-plant-card" ng-if="aiPlantProfile && !aiSearching">
            <div class="gp-ai-card-top">
              <div class="gp-ai-plant-header">
                <div class="gp-verified-row">
                  <span class="gp-badge-gemini">✨ Gemini AI Botanical Verified</span>
                  <span class="gp-ai-category-badge">{{{{aiPlantProfile.category}}}}</span>
                </div>
                <div class="gp-ai-plant-title">
                  {{{{aiPlantProfile.identified_name}}}} 
                  <span class="gp-scientific-name" ng-if="aiPlantProfile.scientific_name">({{{{aiPlantProfile.scientific_name}}}})</span>
                </div>
              </div>

              <!-- Intelligent Autonomous Calibration Display (No manual sliders/inputs) -->
              <div class="gp-ai-threshold-box">
                <div class="gp-threshold-label">
                  <span class="gp-lock-icon">🤖</span>
                  <span>Autonomous Soil Moisture Calibration (AWS IoT Sync):</span>
                </div>
                <div class="gp-threshold-val-row">
                  <div class="gp-threshold-badge">
                    <span class="gp-tb-num">{{{{aiPlantProfile.min_moisture | number:1}}}}%</span>
                    <span class="gp-tb-sub">Min Safe Limit (Wilting Stress)</span>
                  </div>
                  <div class="gp-threshold-arrow">➔</div>
                  <div class="gp-threshold-badge">
                    <span class="gp-tb-num">{{{{aiPlantProfile.max_moisture | number:1}}}}%</span>
                    <span class="gp-tb-sub">Max Safe Limit (Root Rot Risk)</span>
                  </div>
                </div>
                <div class="gp-threshold-note">
                  ✓ Calculated by Gemini AI based on root-zone transpiration science. Automatically persisted to AWS DynamoDB. No manual adjustment required.
                </div>
              </div>
            </div>

            <div class="gp-ai-details-grid">
              <div class="gp-ai-detail-item">
                <span class="gp-adi-icon">{SVG_SUN}</span>
                <div>
                  <div class="gp-adi-title">Sunlight Requirement</div>
                  <div class="gp-adi-val">{{{{aiPlantProfile.sunlight}}}}</div>
                </div>
              </div>

              <div class="gp-ai-detail-item">
                <span class="gp-adi-icon">{SVG_DROPLET}</span>
                <div>
                  <div class="gp-adi-title">Watering Frequency</div>
                  <div class="gp-adi-val">{{{{aiPlantProfile.watering_frequency}}}}</div>
                </div>
              </div>
            </div>

            <div class="gp-ai-summary-box">
              <div class="gp-summary-label">Botanical Care Profile:</div>
              <p class="gp-summary-text">{{{{aiPlantProfile.botanical_summary}}}}</p>
            </div>
          </div>

        </div>

        <!-- Step 2: Location & GPS Module Auto-Detection -->
        <div class="gp-form-section">
          <div class="gp-section-title">
            <span class="gp-step-num">2</span>
            <span>Microclimate Location & GPS Acquisition:</span>
          </div>

          <div class="gp-gps-card">
            <div class="gp-gps-top">
              <div class="gp-gps-status">
                <span class="gp-gps-icon" ng-class="{{'gps-locked': gpsAcquired, 'gps-searching': !gpsAcquired}}">
                  {SVG_SATELLITE}
                </span>
                <div>
                  <div class="gp-gps-title">{{{{gpsStatusText}}}}</div>
                  <div class="gp-gps-coords" ng-if="gpsCoordinates">{{{{gpsCoordinates}}}}</div>
                </div>
              </div>
              <button type="button" class="gp-btn gp-btn-gps" ng-click="triggerGpsDetection()" ng-disabled="gpsLoading">
                <span>{{{{gpsLoading ? 'Acquiring GPS Signal...' : '🛰️ Auto-Detect via GPS Module'}}}}</span>
              </button>
            </div>

            <!-- Quick City Selector -->
            <div style="margin-top: 14px;">
              <label class="gp-form-label">Or Select Microclimate Weather Station (Sri Lanka):</label>
              <div class="gp-city-chips">
                <button type="button" class="gp-chip-sm" 
                        ng-repeat="city in quickCities" 
                        ng-class="{{'chip-active': regData.location_name === city}}" 
                        ng-click="setCity(city)">
                  {{{{city}}}}
                </button>
              </div>
            </div>

            <!-- Live Weather Preview Badge -->
            <div class="gp-weather-preview" ng-if="weatherPreview">
              <div class="gp-wp-city">{SVG_MAPPIN} {{{{weatherPreview.city}}}} Live Forecast:</div>
              <div class="gp-wp-val">{{{{weatherPreview.temp}}}}°C • {{{{weatherPreview.description}}}}</div>
              <div class="gp-wp-rain" ng-class="{{'rain-alert': weatherPreview.rain_expected, 'rain-clear': !weatherPreview.rain_expected}}">
                {{{{weatherPreview.rain_expected ? '🌧️ Rain expected in next 24h (Irrigation delay advised)' : '☀️ Clear skies expected'}}}}
              </div>
            </div>
          </div>
        </div>

        <!-- Step 3: Physical Hardware Verification -->
        <div class="gp-form-section">
          <div class="gp-section-title">
            <span class="gp-step-num">3</span>
            <span>Physical Hardware Verification:</span>
          </div>
          <div class="gp-check-card">
            <label class="gp-checkbox-label">
              <input type="checkbox" ng-model="hardwareConfirmed" required>
              <span>I confirm that the physical ESP32 soil moisture probe and DS18B20 temperature sensor have been firmly planted into <strong>{{{{aiPlantProfile ? aiPlantProfile.identified_name : regData.plant_name}}}}</strong>'s soil root zone (3–4 inches deep).</span>
            </label>
          </div>
        </div>

        <!-- Submit Button -->
        <div class="gp-reg-actions">
          <button type="submit" class="gp-btn gp-btn-register" ng-disabled="!hardwareConfirmed || !regData.plant_name || isSubmitting || !aiPlantProfile">
            <span>{{{{isSubmitting ? 'Registering & Syncing with AWS DynamoDB...' : '🌿 Complete AI Registration & Launch Live Monitor'}}}}</span>
          </button>
        </div>

      </form>

    </div>
  </div>


  <!-- ======================================================== -->
  <!-- VIEW 2: LIVE MONITORING & BOTANICAL INTELLIGENCE MONITOR -->
  <!-- ======================================================== -->
  <div class="gp-dashboard-view" ng-show="viewMode === 'dashboard'">

    <!-- TOP NAVIGATION BAR -->
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
          <span class="gp-dot-live" ng-class="{{'pulse-emerald': hasReceivedTelemetry, 'dot-waiting': !hasReceivedTelemetry}}"></span>
          <span>ESP32: <strong>{{{{activeDeviceId}}}}</strong></span>
        </div>
        <div class="gp-pill" ng-class="{{'gp-pill-aws': hasReceivedTelemetry, 'gp-pill-device': !hasReceivedTelemetry}}">
          <span class="gp-dot-live" ng-class="{{'pulse-emerald': hasReceivedTelemetry, 'dot-waiting': !hasReceivedTelemetry}}"></span>
          <span>{{{{hasReceivedTelemetry ? 'AWS IoT Core (Port 8883) CONNECTED' : 'Waiting for ESP32 Live Stream'}}}}</span>
        </div>
      </div>

      <div class="gp-header-actions">
        <div class="gp-clock">
          <div class="gp-clock-time">{{{{currentTime}}}}</div>
          <div class="gp-clock-zone">Sri Lanka Standard Time</div>
        </div>

        <!-- Prominent Plant Switch / Relocation Button -->
        <button class="gp-btn gp-btn-switch-plant" ng-click="openRelocationModal()">
          {SVG_SHUFFLE}
          <span>Switch Plant / Move Device</span>
        </button>
      </div>
    </header>

    <!-- ACTIVE PLANT & CITY WEATHER BANNER -->
    <section class="gp-meta-grid">
      <!-- Active Plant Card -->
      <div class="gp-meta-card gp-plant-card">
        <div class="gp-meta-icon-box gp-icon-emerald">
          {SVG_SPROUT}
        </div>
        <div class="gp-meta-info">
          <div class="gp-meta-label">Active Plant Species</div>
          <div class="gp-meta-val-row">
            <span class="gp-meta-title">{{{{plant.plant_name || 'Tomato'}}}} <span class="gp-sub-sci" ng-if="plant.scientific_name">({{{{plant.scientific_name}}}})</span></span>
            <span class="gp-badge gp-badge-emerald">Safe Root Zone: {{{{plant.min_moisture}}}}% – {{{{plant.max_moisture}}}}%</span>
          </div>
          <div class="gp-meta-desc">{{{{plant.notes || 'Target botanical parameters autonomously guarded by Gemini AI'}}}}</div>
        </div>
        <button class="gp-btn-switch" ng-click="openRelocationModal()">
          {SVG_SHUFFLE}
          <span>Move Device</span>
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

    <!-- 6 SENSOR TELEMETRY CARDS -->
    <section class="gp-sensors-grid">
      <!-- 1. Soil Moisture -->
      <div class="gp-card gp-card-metric" ng-class="{{'border-alert': hasReceivedTelemetry && sensor.soil_moisture < plant.min_moisture, 'border-optimal': hasReceivedTelemetry && sensor.soil_moisture >= plant.min_moisture && sensor.soil_moisture <= plant.max_moisture}}">
        <div class="gp-card-header">
          <span class="gp-card-icon gp-icon-emerald">{SVG_DROPLET}</span>
          <span class="gp-card-tag" ng-class="{{'tag-opt': hasReceivedTelemetry && sensor.soil_moisture >= plant.min_moisture && sensor.soil_moisture <= plant.max_moisture, 'tag-warn': hasReceivedTelemetry && sensor.soil_moisture < plant.min_moisture, 'tag-wait': !hasReceivedTelemetry}}">
            {{{{hasReceivedTelemetry ? (sensor.soil_moisture >= plant.min_moisture ? 'Optimal Hydration' : 'Water Deficit') : 'Awaiting Data'}}}}
          </span>
        </div>
        <div class="gp-metric-val">{{{{hasReceivedTelemetry && sensor.soil_moisture !== null ? (sensor.soil_moisture | number:1) : '--'}}}}<span class="gp-unit">%</span></div>
        <div class="gp-metric-name">Soil Moisture (Root Level)</div>
        <div class="gp-bar-track">
          <div class="gp-bar-fill gp-fill-emerald" style="width: {{{{hasReceivedTelemetry && sensor.soil_moisture !== null ? sensor.soil_moisture : 0}}}}%;"></div>
        </div>
        <div class="gp-range-hint">Safe Target: {{{{plant.min_moisture}}}}% – {{{{plant.max_moisture}}}}%</div>
      </div>

      <!-- 2. Soil Temperature (DS18B20) -->
      <div class="gp-card gp-card-metric">
        <div class="gp-card-header">
          <span class="gp-card-icon gp-icon-teal">{SVG_PROBE}</span>
          <span class="gp-card-tag" ng-class="{{'tag-opt': hasReceivedTelemetry, 'tag-wait': !hasReceivedTelemetry}}">{{{{hasReceivedTelemetry ? 'Sub-surface Probe' : 'Awaiting Data'}}}}</span>
        </div>
        <div class="gp-metric-val">{{{{hasReceivedTelemetry && sensor.soil_temperature !== null ? (sensor.soil_temperature | number:1) : '--'}}}}<span class="gp-unit">°C</span></div>
        <div class="gp-metric-name">Soil Temperature (DS18B20)</div>
        <div class="gp-bar-track">
          <div class="gp-bar-fill gp-fill-teal" style="width: {{{{hasReceivedTelemetry && sensor.soil_temperature !== null ? ((sensor.soil_temperature / 45) * 100) : 0}}}}%;"></div>
        </div>
        <div class="gp-range-hint">Root Comfort: 18.0°C – 28.0°C</div>
      </div>

      <!-- 3. Ambient Temperature (DHT22) -->
      <div class="gp-card gp-card-metric">
        <div class="gp-card-header">
          <span class="gp-card-icon gp-icon-amber">{SVG_THERMO}</span>
          <span class="gp-card-tag" ng-class="{{'tag-opt': hasReceivedTelemetry && sensor.temperature <= 32, 'tag-warn': hasReceivedTelemetry && sensor.temperature > 32, 'tag-wait': !hasReceivedTelemetry}}">
            {{{{hasReceivedTelemetry ? (sensor.temperature <= 32 ? 'Optimal Thermal' : 'Heat Warning') : 'Awaiting Data'}}}}
          </span>
        </div>
        <div class="gp-metric-val">{{{{hasReceivedTelemetry && sensor.temperature !== null ? (sensor.temperature | number:1) : '--'}}}}<span class="gp-unit">°C</span></div>
        <div class="gp-metric-name">Ambient Temperature (DHT22)</div>
        <div class="gp-bar-track">
          <div class="gp-bar-fill gp-fill-amber" style="width: {{{{hasReceivedTelemetry && sensor.temperature !== null ? ((sensor.temperature / 45) * 100) : 0}}}}%;"></div>
        </div>
        <div class="gp-range-hint">Threshold Ceiling: 33.0°C</div>
      </div>

      <!-- 4. Ambient Humidity (DHT22) -->
      <div class="gp-card gp-card-metric">
        <div class="gp-card-header">
          <span class="gp-card-icon gp-icon-blue">{SVG_CLOUD}</span>
          <span class="gp-card-tag" ng-class="{{'tag-opt': hasReceivedTelemetry, 'tag-wait': !hasReceivedTelemetry}}">{{{{hasReceivedTelemetry ? 'Air Moisture' : 'Awaiting Data'}}}}</span>
        </div>
        <div class="gp-metric-val">{{{{hasReceivedTelemetry && sensor.humidity !== null ? (sensor.humidity | number:1) : '--'}}}}<span class="gp-unit">%</span></div>
        <div class="gp-metric-name">Relative Humidity (DHT22)</div>
        <div class="gp-bar-track">
          <div class="gp-bar-fill gp-fill-blue" style="width: {{{{hasReceivedTelemetry && sensor.humidity !== null ? sensor.humidity : 0}}}}%;"></div>
        </div>
        <div class="gp-range-hint">Normal Transpiration: 40% – 70%</div>
      </div>

      <!-- 5. Air Quality MQ Sensor -->
      <div class="gp-card gp-card-metric">
        <div class="gp-card-header">
          <span class="gp-card-icon gp-icon-cyan">{SVG_WIND}</span>
          <span class="gp-card-tag" ng-class="{{'tag-opt': hasReceivedTelemetry, 'tag-wait': !hasReceivedTelemetry}}">{{{{hasReceivedTelemetry ? 'Gas & Purity' : 'Awaiting Data'}}}}</span>
        </div>
        <div class="gp-metric-val">{{{{hasReceivedTelemetry && sensor.air_quality_percent !== null ? (sensor.air_quality_percent | number:0) : '--'}}}}<span class="gp-unit">%</span></div>
        <div class="gp-metric-name">Air Quality Level (MQ)</div>
        <div class="gp-bar-track">
          <div class="gp-bar-fill gp-fill-cyan" style="width: {{{{hasReceivedTelemetry && sensor.air_quality_percent !== null ? sensor.air_quality_percent : 0}}}}%;"></div>
        </div>
        <div class="gp-range-hint">Purity Status: Pure & Clean Air</div>
      </div>

      <!-- 6. Barometric Pressure (BMP280) -->
      <div class="gp-card gp-card-metric">
        <div class="gp-card-header">
          <span class="gp-card-icon gp-icon-purple">{SVG_GAUGE}</span>
          <span class="gp-card-tag" ng-class="{{'tag-opt': hasReceivedTelemetry, 'tag-wait': !hasReceivedTelemetry}}">{{{{hasReceivedTelemetry ? 'BMP280 I2C' : 'Awaiting Data'}}}}</span>
        </div>
        <div class="gp-metric-val">{{{{hasReceivedTelemetry && sensor.air_pressure !== null ? (sensor.air_pressure | number:1) : '--'}}}}<span class="gp-unit">hPa</span></div>
        <div class="gp-metric-name">Barometric Pressure</div>
        <div class="gp-bar-track">
          <div class="gp-bar-fill gp-fill-purple" style="width: {{{{hasReceivedTelemetry && sensor.air_pressure !== null ? (((sensor.air_pressure - 950) / 100) * 100) : 0}}}}%;"></div>
        </div>
        <div class="gp-range-hint">Standard Atmosphere: ~1013.25 hPa</div>
      </div>
    </section>

    <!-- TELEMETRY TRENDS & AI DOCTOR ROW -->
    <section class="gp-intelligence-grid">
      <!-- Real-time Trends Line Graph Card -->
      <div class="gp-card gp-chart-card">
        <div class="gp-chart-header">
          <div class="gp-chart-title-row">
            <span class="gp-intel-icon gp-icon-teal">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
            </span>
            <div>
              <div class="gp-intel-title">Multi-Sensor Telemetry Trends</div>
              <div class="gp-intel-sub">Live 60-Second Real-time Sensor Stream for {{{{plant.plant_name}}}}</div>
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

          <button class="gp-btn gp-btn-ai-run" ng-click="runAiDiagnosis()" ng-disabled="aiLoading || !hasReceivedTelemetry">
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
          <span>Physical Telemetry: {{{{hasReceivedTelemetry ? 'Live Stream' : 'Awaiting ESP32'}}}}</span>
        </div>
      </div>
    </section>

  </div>


  <!-- ======================================================== -->
  <!-- MODAL: PHYSICAL HARDWARE SENSOR RELOCATION PROTOCOL     -->
  <!-- ======================================================== -->
  <div class="gp-modal-backdrop" ng-if="showRelocationModal" ng-click="closeRelocationModal($event)">
    <div class="gp-modal-content gp-relocate-modal" ng-click="$event.stopPropagation()">
      
      <div class="gp-modal-header gp-modal-header-warn">
        <div class="gp-modal-title-row">
          <span class="gp-icon-amber">{SVG_ALERT}</span>
          <h3>Physical Hardware Sensor Relocation Protocol</h3>
        </div>
        <button class="gp-modal-close" ng-click="closeRelocationModal()">✕</button>
      </div>

      <div class="gp-modal-body">
        <div class="gp-warn-banner">
          <strong>CRITICAL HARDWARE STEP REQUIRED BEFORE REGISTERING NEW PLANT:</strong>
          <p>You are about to switch monitoring from <strong>{{{{plant.plant_name}}}}</strong> to a new plant. You MUST physically move your ESP32 sensors to ensure accurate telemetry and prevent false AI care diagnoses.</p>
        </div>

        <div class="gp-relocate-steps">
          <div class="gp-r-step">
            <div class="gp-r-num">1</div>
            <div><strong>Extract Sensor Probes:</strong> Gently withdraw the capacitive soil moisture sensor and DS18B20 stainless steel probe from the current ({{{{plant.plant_name}}}}) pot.</div>
          </div>
          <div class="gp-r-step">
            <div class="gp-r-num">2</div>
            <div><strong>Clean the Probes:</strong> Wipe probe tips dry with clean tissue to remove mineral buildup and cross-contaminating root microbes.</div>
          </div>
          <div class="gp-r-step">
            <div class="gp-r-num">3</div>
            <div><strong>Insert in New Target Plant:</strong> Push both probes 3 to 4 inches deep into the soil of your new target plant near the root zone.</div>
          </div>
          <div class="gp-r-step">
            <div class="gp-r-num">4</div>
            <div><strong>Verify ESP32 Power:</strong> Confirm the ESP32 board is securely powered and Wi-Fi indicator stays on.</div>
          </div>
        </div>

        <div class="gp-check-card" style="margin-top: 20px;">
          <label class="gp-checkbox-label">
            <input type="checkbox" ng-model="relocationConfirmed">
            <span><strong>I confirm that I have physically relocated and planted the ESP32 probes into the new plant's soil.</strong></span>
          </label>
        </div>
      </div>

      <div class="gp-modal-footer">
        <button type="button" class="gp-btn gp-btn-secondary" ng-click="closeRelocationModal()">Cancel (Keep Monitoring {{{{plant.plant_name}}}})</button>
        <button type="button" class="gp-btn gp-btn-danger" ng-disabled="!relocationConfirmed" ng-click="confirmRelocationAndRegister()">
          <span>Proceed to Register New Plant ➔</span>
        </button>
      </div>

    </div>
  </div>

</div>


<!-- ================= MODERN LIGHT STYLES ================= -->
<style>
html, body, md-content, .nr-dashboard-theme {{
  background-color: #f8fafc !important;
  color: #0f172a !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif !important;
  margin: 0 !important;
  padding: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  overflow: hidden !important;
}}

md-toolbar.nr-dashboard-toolbar {{
  display: none !important;
}}

#gp-app.gp-dashboard {{
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  z-index: 9999 !important;
  background-color: #f8fafc !important;
  box-sizing: border-box !important;
  padding: 24px 36px 60px 36px !important;
}}

/* Registration Card Layout */
.gp-reg-container {{
  max-width: 900px;
  margin: 20px auto;
  animation: fadeIn 0.3s ease;
}}
.gp-reg-card {{
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.06);
  padding: 32px 36px;
}}
.gp-reg-header {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 22px;
  border-bottom: 1px solid #f1f5f9;
  margin-bottom: 26px;
}}
.gp-form-section {{
  margin-bottom: 28px;
}}
.gp-section-title {{
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 15px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 14px;
}}
.gp-step-num {{
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: #10b981;
  color: #ffffff;
  font-size: 12px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
}}
/* AI Search Bar */
.gp-search-box-wrap {{
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  padding: 18px 20px;
}}
.gp-search-input-row {{
  display: flex;
  gap: 12px;
}}
.gp-input-search {{
  flex: 1;
  font-size: 15px !important;
  padding: 13px 18px !important;
  border: 1.5px solid #cbd5e1 !important;
  border-radius: 12px !important;
  background: #ffffff !important;
  color: #0f172a !important;
}}
.gp-input-search:focus {{
  border-color: #10b981 !important;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15) !important;
  outline: none;
}}
.gp-btn-ai-search {{
  background: linear-gradient(135deg, #059669 0%, #10b981 100%) !important;
  color: #ffffff !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 0 24px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.28);
}}
.gp-btn-ai-search:hover:not(:disabled) {{
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(16, 185, 129, 0.38);
}}
.gp-btn-ai-search:disabled {{
  opacity: 0.6;
  cursor: not-allowed;
}}
.gp-quick-search-tags {{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 14px;
}}
.gp-quick-label {{
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  margin-right: 4px;
}}
.gp-tag-chip {{
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 20px;
  padding: 6px 13px;
  font-size: 12px;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
  transition: all 0.2s;
}}
.gp-tag-chip:hover {{
  border-color: #10b981;
  color: #059669;
  background: #ecfdf5;
}}
.gp-ai-identifying-banner {{
  display: flex;
  align-items: center;
  gap: 16px;
  background: #ecfdf5;
  border: 1.5px dashed #10b981;
  border-radius: 14px;
  padding: 16px 20px;
  margin-top: 16px;
  color: #065f46;
  animation: pulse 1.8s infinite;
}}
.gp-spin-glow {{
  color: #10b981;
  animation: spin 2s linear infinite;
}}
.gp-ai-plant-card {{
  background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
  border: 1.5px solid #10b981;
  border-radius: 18px;
  padding: 24px;
  margin-top: 18px;
  box-shadow: 0 10px 30px rgba(16, 185, 129, 0.1);
  animation: fadeIn 0.3s ease;
}}
.gp-verified-row {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}}
.gp-badge-gemini {{
  background: #10b981;
  color: #ffffff;
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 20px;
  letter-spacing: 0.3px;
}}
.gp-ai-category-badge {{
  background: #d1fae5;
  color: #047857;
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
}}
.gp-ai-plant-title {{
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
}}
.gp-scientific-name {{
  font-size: 16px;
  font-style: italic;
  font-weight: 600;
  color: #059669;
}}
.gp-sub-sci {{
  font-size: 13px;
  font-style: italic;
  font-weight: 500;
  color: #64748b;
  margin-left: 6px;
}}
.gp-ai-threshold-box {{
  background: #ffffff;
  border: 1.5px solid #a7f3d0;
  border-radius: 14px;
  padding: 16px 20px;
  margin-top: 16px;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.06);
}}
.gp-threshold-label {{
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 800;
  color: #065f46;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}}
.gp-threshold-val-row {{
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 10px;
}}
.gp-threshold-badge {{
  flex: 1;
  background: #ecfdf5;
  border: 1px solid #10b981;
  border-radius: 12px;
  padding: 10px 16px;
  text-align: center;
}}
.gp-tb-num {{
  font-size: 22px;
  font-weight: 900;
  color: #047857;
  display: block;
}}
.gp-tb-sub {{
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
}}
.gp-threshold-arrow {{
  font-size: 18px;
  font-weight: 900;
  color: #10b981;
}}
.gp-threshold-note {{
  font-size: 12px;
  color: #047857;
  font-weight: 600;
  margin-top: 10px;
}}
.gp-ai-details-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 16px;
}}
@media (max-width: 600px) {{
  .gp-ai-details-grid {{ grid-template-columns: 1fr; }}
}}
.gp-ai-detail-item {{
  display: flex;
  align-items: center;
  gap: 12px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 16px;
}}
.gp-adi-icon {{
  color: #10b981;
}}
.gp-adi-title {{
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  color: #64748b;
}}
.gp-adi-val {{
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
  margin-top: 2px;
}}
.gp-ai-summary-box {{
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 14px 18px;
  margin-top: 14px;
}}
.gp-summary-label {{
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  color: #059669;
}}
.gp-summary-text {{
  font-size: 13px;
  color: #334155;
  line-height: 1.5;
  margin: 6px 0 0 0;
}}

/* GPS Card */
.gp-gps-card {{
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 18px 20px;
}}
.gp-gps-top {{
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.gp-gps-status {{
  display: flex;
  align-items: center;
  gap: 12px;
}}
.gp-gps-icon {{
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e2e8f0;
  color: #475569;
}}
.gps-locked {{
  background: #ecfdf5 !important;
  color: #059669 !important;
}}
.gp-gps-title {{
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
}}
.gp-gps-coords {{
  font-size: 11px;
  color: #059669;
  font-family: monospace;
  font-weight: 700;
}}
.gp-btn-gps {{
  background: #0f172a;
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 10px;
  font-size: 12px;
}}
.gp-btn-gps:hover {{
  background: #059669;
}}

.gp-weather-preview {{
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 14px;
  padding: 10px 14px;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  font-size: 12px;
}}
.gp-wp-city {{ font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 4px; }}
.gp-wp-val {{ font-weight: 600; color: #334155; }}
.gp-wp-rain {{ font-weight: 700; margin-left: auto; }}

/* Checkbox Card */
.gp-check-card {{
  background: #f8fafc;
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  padding: 14px 18px;
}}
.gp-checkbox-label {{
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 13px;
  line-height: 1.5;
  color: #334155;
  cursor: pointer;
}}
.gp-checkbox-label input {{
  margin-top: 3px;
  width: 18px;
  height: 18px;
  accent-color: #059669;
}}

.gp-reg-actions {{
  margin-top: 30px;
}}
.gp-btn-register {{
  width: 100%;
  padding: 16px;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 800;
  background: linear-gradient(135deg, #059669 0%, #10b981 100%);
  color: #ffffff;
  border: none;
  cursor: pointer;
  box-shadow: 0 6px 20px rgba(5, 150, 105, 0.35);
  transition: all 0.2s;
}}
.gp-btn-register:hover:not(:disabled) {{
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(5, 150, 105, 0.45);
}}
.gp-btn-register:disabled {{
  opacity: 0.5;
  cursor: not-allowed;
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
.gp-brand {{ display: flex; align-items: center; gap: 14px; }}
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
.gp-title {{ font-size: 20px; font-weight: 800; letter-spacing: -0.5px; color: #0f172a; }}
.gp-accent {{ color: #059669; }}
.gp-subtitle {{ font-size: 12px; color: #64748b; font-weight: 500; }}
.gp-header-center {{ display: flex; gap: 12px; align-items: center; }}
.gp-pill {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 16px;
  border-radius: 30px;
  font-size: 12px;
  font-weight: 600;
}}
.gp-pill-device {{ background: #f1f5f9; border: 1px solid #e2e8f0; color: #334155; }}
.gp-pill-aws {{ background: #ecfdf5; border: 1px solid #a7f3d0; color: #047857; }}
.gp-dot-live {{ width: 8px; height: 8px; border-radius: 50%; background: #10b981; }}
.pulse-emerald {{ box-shadow: 0 0 10px #10b981; animation: pulseDot 2s infinite; }}
.dot-waiting {{ background: #94a3b8 !important; box-shadow: none !important; animation: none !important; }}
@keyframes pulseDot {{
  0% {{ transform: scale(0.9); opacity: 0.8; }}
  50% {{ transform: scale(1.3); opacity: 1; }}
  100% {{ transform: scale(0.9); opacity: 0.8; }}
}}

.gp-header-actions {{ display: flex; align-items: center; gap: 20px; }}
.gp-clock {{ text-align: right; }}
.gp-clock-time {{ font-size: 16px; font-weight: 700; color: #0f172a; }}
.gp-clock-zone {{ font-size: 11px; color: #64748b; }}

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
.gp-btn-switch-plant {{
  background: #0f172a;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
}}
.gp-btn-switch-plant:hover {{
  background: #059669;
  box-shadow: 0 6px 16px rgba(5, 150, 105, 0.25);
  transform: translateY(-1px);
}}

/* Active Plant & City Weather Banner */
.gp-meta-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
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
.gp-plant-card {{ border-left: 5px solid #10b981; }}
.gp-weather-card {{ border-left: 5px solid #06b6d4; }}
.gp-meta-icon-box {{
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}
.gp-icon-emerald {{ background: #ecfdf5; color: #059669; }}
.gp-icon-cyan {{ background: #ecfeff; color: #0891b2; }}
.gp-icon-amber {{ background: #fffbeb; color: #d97706; }}
.gp-icon-teal {{ background: #f0fdfa; color: #0d9488; }}
.gp-icon-blue {{ background: #eff6ff; color: #2563eb; }}
.gp-icon-purple {{ background: #f5f3ff; color: #7c3aed; }}
.gp-icon-sparkle {{ background: linear-gradient(135deg, #ecfdf5 0%, #ecfeff 100%); color: #059669; }}
.gp-meta-info {{ flex: 1; }}
.gp-meta-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; color: #64748b; font-weight: 700; margin-bottom: 3px; }}
.gp-meta-val-row {{ display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }}
.gp-meta-title {{ font-size: 20px; font-weight: 800; color: #0f172a; }}
.gp-weather-cond {{ font-size: 13px; color: #334155; font-weight: 600; }}
.gp-badge {{ padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; }}
.gp-badge-emerald {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
.gp-meta-desc {{ font-size: 12px; color: #64748b; margin-top: 4px; }}
.gp-rain-status {{ display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 600; margin-top: 6px; }}
.rain-alert {{ color: #0284c7; }}
.rain-clear {{ color: #059669; }}
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
.gp-btn-switch:hover {{ background: #059669; color: #ffffff; border-color: #059669; }}

/* 6 Sensors Grid */
.gp-sensors-grid {{
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}}
@media (max-width: 1400px) {{ .gp-sensors-grid {{ grid-template-columns: repeat(3, 1fr); }} }}
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
.gp-card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08); }}
.gp-card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
.gp-card-icon {{ width: 38px; height: 38px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }}
.gp-card-tag {{ font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 6px; }}
.tag-opt {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
.tag-warn {{ background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }}
.tag-wait {{ background: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1; }}
.border-alert {{ border-color: #f59e0b !important; }}
.border-optimal {{ border-color: #10b981 !important; }}
.gp-metric-val {{ font-size: 34px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px; line-height: 1; }}
.gp-unit {{ font-size: 16px; color: #64748b; margin-left: 3px; font-weight: 600; }}
.gp-metric-name {{ font-size: 12px; color: #475569; font-weight: 700; margin-top: 10px; }}
.gp-bar-track {{ width: 100%; height: 7px; background: #f1f5f9; border-radius: 10px; overflow: hidden; margin-top: 10px; }}
.gp-bar-fill {{ height: 100%; border-radius: 10px; transition: width 0.6s ease; }}
.gp-fill-emerald {{ background: linear-gradient(90deg, #10b981, #059669); }}
.gp-fill-teal {{ background: linear-gradient(90deg, #14b8a6, #0d9488); }}
.gp-fill-amber {{ background: linear-gradient(90deg, #f59e0b, #d97706); }}
.gp-fill-blue {{ background: linear-gradient(90deg, #3b82f6, #2563eb); }}
.gp-fill-cyan {{ background: linear-gradient(90deg, #06b6d4, #0891b2); }}
.gp-fill-purple {{ background: linear-gradient(90deg, #8b5cf6, #7c3aed); }}
.gp-range-hint {{ font-size: 10px; color: #94a3b8; font-weight: 500; margin-top: 8px; }}

/* Intelligence Grid */
.gp-intelligence-grid {{ display: grid; grid-template-columns: 1.15fr 1fr; gap: 24px; margin-bottom: 24px; }}
@media (max-width: 1100px) {{ .gp-intelligence-grid {{ grid-template-columns: 1fr; }} }}
.gp-intel-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; padding-bottom: 14px; border-bottom: 1px solid #f1f5f9; }}
.gp-intel-title-row {{ display: flex; align-items: center; gap: 12px; }}
.gp-intel-icon {{ width: 42px; height: 42px; border-radius: 12px; display: flex; align-items: center; justify-content: center; }}
.gp-intel-title {{ font-size: 17px; font-weight: 800; color: #0f172a; }}
.gp-intel-sub {{ font-size: 12px; color: #64748b; }}
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
.gp-btn-ai-run:disabled {{ opacity: 0.6; cursor: not-allowed; }}
.gp-spin {{ display: inline-block; animation: spin 1s linear infinite; }}
@keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
.gp-ai-content {{ min-height: 200px; max-height: 380px; overflow-y: auto; padding: 18px 20px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; }}
.gp-ai-loading-box {{ display: flex; flex-direction: column; align-items: center; justify-content: center; height: 180px; gap: 16px; }}
.gp-pulse-ring {{ width: 42px; height: 42px; border: 4px solid #d1fae5; border-top-color: #059669; border-radius: 50%; animation: spin 0.8s linear infinite; }}
.gp-loading-text {{ font-size: 13px; color: #64748b; font-style: italic; text-align: center; max-width: 420px; }}
.gp-ai-markdown {{ font-size: 13px; line-height: 1.7; color: #1e293b; }}
.gp-ai-markdown h3 {{ color: #047857; font-size: 15px; font-weight: 800; margin: 14px 0 6px 0; border-bottom: 2px solid #a7f3d0; padding-bottom: 4px; }}
.gp-ai-markdown ul {{ margin: 6px 0 12px 20px; padding: 0; }}
.gp-ai-markdown li {{ margin-bottom: 5px; }}
.gp-ai-footer {{ display: flex; justify-content: space-between; margin-top: 14px; font-size: 11px; color: #94a3b8; font-weight: 600; }}

/* Canvas Chart */
.gp-chart-card {{ padding: 24px; }}
.gp-chart-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; flex-wrap: wrap; gap: 12px; }}
.gp-chart-title-row {{ display: flex; align-items: center; gap: 12px; }}
.gp-chart-legend {{ display: flex; gap: 16px; font-size: 12px; color: #334155; font-weight: 600; }}
.gp-legend-item {{ display: flex; align-items: center; gap: 6px; }}
.dot-emerald {{ width: 10px; height: 10px; border-radius: 50%; background: #059669; }}
.dot-teal {{ width: 10px; height: 10px; border-radius: 50%; background: #0d9488; }}
.dot-amber {{ width: 10px; height: 10px; border-radius: 50%; background: #d97706; }}
.dot-blue {{ width: 10px; height: 10px; border-radius: 50%; background: #2563eb; }}
.gp-chart-canvas-wrap {{ position: relative; width: 100%; height: 240px; }}

/* Form Elements */
.gp-form-row {{ display: flex; gap: 16px; }}
.gp-col-6 {{ flex: 1; }}
.gp-col-12 {{ width: 100%; }}
.gp-form-group {{ margin-bottom: 14px; }}
.gp-form-label {{ display: block; font-size: 12px; font-weight: 700; color: #475569; margin-bottom: 6px; }}
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
.gp-input:focus {{ border-color: #059669; box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.15); }}
.gp-hint {{ font-size: 11px; color: #94a3b8; margin-top: 4px; display: block; }}
.gp-city-chips {{ display: flex; flex-wrap: wrap; gap: 6px; }}
.gp-chip-sm {{
  padding: 5px 12px;
  border-radius: 14px;
  font-size: 11px;
  font-weight: 600;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  color: #475569;
  cursor: pointer;
}}
.gp-chip-sm:hover {{ color: #0284c7; border-color: #38bdf8; background: #f0f9ff; }}
.chip-active {{ background: #0f172a !important; color: #ffffff !important; border-color: #0f172a !important; }}

/* Relocation Modal */
.gp-modal-backdrop {{
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.7);
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
  max-width: 640px;
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
.gp-modal-header-warn {{ background: #fffbeb !important; border-bottom: 1px solid #fef3c7 !important; }}
.gp-modal-title-row {{ display: flex; align-items: center; gap: 10px; }}
.gp-modal-title-row h3 {{ margin: 0; font-size: 17px; font-weight: 800; color: #0f172a; }}
.gp-modal-close {{ background: none; border: none; color: #64748b; font-size: 18px; cursor: pointer; padding: 4px 8px; border-radius: 6px; }}
.gp-modal-body {{ padding: 24px; }}
.gp-warn-banner {{
  background: #fef2f2;
  border-left: 4px solid #ef4444;
  padding: 14px 16px;
  border-radius: 8px;
  font-size: 13px;
  color: #991b1b;
  line-height: 1.5;
  margin-bottom: 20px;
}}
.gp-warn-banner strong {{ color: #7f1d1d; display: block; margin-bottom: 4px; font-size: 13px; }}
.gp-relocate-steps {{ display: flex; flex-direction: column; gap: 12px; }}
.gp-r-step {{
  display: flex;
  gap: 12px;
  align-items: flex-start;
  font-size: 13px;
  color: #334155;
  line-height: 1.5;
}}
.gp-r-num {{
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #0f172a;
  color: #ffffff;
  font-size: 11px;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}
.gp-modal-footer {{
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  background: #f8fafc;
  border-top: 1px solid #e2e8f0;
}}
.gp-btn-secondary {{ background: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; }}
.gp-btn-danger {{
  background: #dc2626;
  color: #ffffff;
  border: none;
}}
.gp-btn-danger:hover:not(:disabled) {{ background: #b91c1c; }}
.gp-btn-danger:disabled {{ opacity: 0.5; cursor: not-allowed; }}
</style>


<!-- ================= EMBEDDED CONTROLLER ================= -->
<script>
(function(scope) {{

  scope.activeDeviceId = 'greenpulse-team-infinix';
  scope.viewMode = 'register'; // 'register' or 'dashboard'
  scope.hasReceivedTelemetry = false;
  scope.hardwareConfirmed = false;
  scope.isSubmitting = false;

  scope.presets = {{
    "Tomato": {{"min_moisture": 50.0, "max_moisture": 75.0, "notes": "High moisture requirement, steady hydration"}},
    "Rose": {{"min_moisture": 30.0, "max_moisture": 70.0, "notes": "Moderate moisture, thrives in sun"}},
    "Monstera": {{"min_moisture": 35.0, "max_moisture": 65.0, "notes": "Allow surface soil to dry slightly"}},
    "Chili / Pepper": {{"min_moisture": 45.0, "max_moisture": 70.0, "notes": "Warm conditions, steady watering"}},
    "Mint": {{"min_moisture": 55.0, "max_moisture": 75.0, "notes": "Loves moist soil, fast growing"}},
    "Fern": {{"min_moisture": 60.0, "max_moisture": 80.0, "notes": "High humidity and damp root zone"}},
    "Cactus": {{"min_moisture": 10.0, "max_moisture": 30.0, "notes": "Drought tolerant, dry medium"}},
    "Succulent": {{"min_moisture": 15.0, "max_moisture": 35.0, "notes": "Allow dry-out between waterings"}},
    "Orchid": {{"min_moisture": 25.0, "max_moisture": 50.0, "notes": "Epiphytic, well-draining bark"}}
  }};

  scope.quickCities = ["Colombo", "Kandy", "Galle", "Kurunegala", "Negombo", "Gampaha", "Nuwara Eliya", "Jaffna"];

  // AI Plant Search & Autonomous Calibration State
  scope.plantSearchQuery = "Snake Plant";
  scope.aiSearching = false;
  scope.aiPlantProfile = null;

  // Registration Form State
  scope.regData = {{
    plant_name: "Snake Plant",
    scientific_name: "Dracaena trifasciata",
    category: "Asparagaceae / Succulent Foliage",
    location_name: "Colombo",
    min_moisture: 20.0,
    max_moisture: 45.0,
    sunlight: "Low to bright indirect light",
    watering_frequency: "Every 2 to 4 weeks",
    notes: "Resilient drought-tolerant plant"
  }};

  // Active Monitoring Plant State
  scope.plant = {{
    plant_name: "Snake Plant",
    scientific_name: "Dracaena trifasciata",
    category: "Asparagaceae / Succulent Foliage",
    location_name: "Colombo",
    min_moisture: 20.0,
    max_moisture: 45.0,
    sunlight: "Low to bright indirect light",
    watering_frequency: "Every 2 to 4 weeks",
    notes: ""
  }};

  scope.weather = {{
    city: "Colombo",
    temp: 27.0,
    humidity: 85,
    description: "Scattered Clouds",
    rain_expected: true
  }};

  scope.weatherPreview = null;

  scope.sensor = {{
    device_id: scope.activeDeviceId,
    soil_moisture: null,
    soil_temperature: null,
    temperature: null,
    humidity: null,
    air_quality_percent: null,
    air_pressure: null,
    timestamp: null
  }};

  scope.gpsLoading = false;
  scope.gpsAcquired = false;
  scope.gpsStatusText = "GPS Module Ready for Satellite Acquisition";
  scope.gpsCoordinates = null;

  // Relocation Modal State
  scope.showRelocationModal = false;
  scope.relocationConfirmed = false;

  scope.currentTime = new Date().toLocaleTimeString();
  setInterval(function() {{
    scope.currentTime = new Date().toLocaleTimeString();
    scope.$applyAsync();
  }}, 1000);

  // Initialize
  scope.init = function() {{
    var savedReg = localStorage.getItem('gp_plant_registered');
    if (savedReg === 'true') {{
      scope.viewMode = 'dashboard';
    }} else {{
      scope.viewMode = 'register';
      scope.searchAndIdentifyPlant();
    }}

    scope.fetchBackendConfig();
    scope.initChart();
  }};

  scope.quickSelectPlant = function(name) {{
    scope.plantSearchQuery = name;
    scope.searchAndIdentifyPlant();
  }};

  // Gemini 3.8 Flash Plant Identification & Moisture Calibration
  scope.searchAndIdentifyPlant = function() {{
    if (!scope.plantSearchQuery) return;
    scope.aiSearching = true;

    fetch('http://localhost:5005/api/ai/identify-plant', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ plant_name: scope.plantSearchQuery }})
    }})
    .then(function(res) {{ return res.json(); }})
    .then(function(data) {{
      scope.aiSearching = false;
      if (data && data.plant) {{
        scope.aiPlantProfile = data.plant;
        // Auto-assign into registration data model
        scope.regData.plant_name = data.plant.identified_name;
        scope.regData.scientific_name = data.plant.scientific_name;
        scope.regData.category = data.plant.category;
        scope.regData.min_moisture = data.plant.min_moisture;
        scope.regData.max_moisture = data.plant.max_moisture;
        scope.regData.sunlight = data.plant.sunlight;
        scope.regData.watering_frequency = data.plant.watering_frequency;
        scope.regData.notes = data.plant.botanical_summary;
      }}
      scope.$applyAsync();
    }})
    .catch(function(err) {{
      console.warn("AI Identify call error, using local heuristic:", err);
      scope.aiSearching = false;
      scope.aiPlantProfile = {{
        identified_name: scope.plantSearchQuery,
        scientific_name: "Botanical cultivar",
        category: "Tropical / Foliage",
        min_moisture: 30.0,
        max_moisture: 65.0,
        sunlight: "Bright Indirect Sunlight",
        watering_frequency: "Water when top 1-2 inches dry",
        botanical_summary: "Autonomous botanical profile for " + scope.plantSearchQuery
      }};
      scope.regData.plant_name = scope.aiPlantProfile.identified_name;
      scope.regData.scientific_name = scope.aiPlantProfile.scientific_name;
      scope.regData.min_moisture = scope.aiPlantProfile.min_moisture;
      scope.regData.max_moisture = scope.aiPlantProfile.max_moisture;
      scope.regData.notes = scope.aiPlantProfile.botanical_summary;
      scope.$applyAsync();
    }});
  }};

  scope.setCity = function(city) {{
    scope.regData.location_name = city;
    scope.fetchWeatherPreview(city);
  }};

  // GPS Module Detection Simulation & Geolocation
  scope.triggerGpsDetection = function() {{
    scope.gpsLoading = true;
    scope.gpsStatusText = "Pinging GPS Satellites & Acquiring NMEA sentences...";
    
    // Check browser geolocation or simulate GPS receiver module fix
    if (navigator.geolocation) {{
      navigator.geolocation.getCurrentPosition(
        function(pos) {{
          var lat = pos.coords.latitude.toFixed(4);
          var lon = pos.coords.longitude.toFixed(4);
          scope.gpsLoading = false;
          scope.gpsAcquired = true;
          scope.gpsCoordinates = lat + "° N, " + lon + "° E (Satellites: 9 | HDOP: 0.9)";
          scope.gpsStatusText = "GPS 3D Fix Locked (Accuracy: ±" + Math.round(pos.coords.accuracy) + "m)";
          scope.setCity("Colombo");
          scope.$applyAsync();
        }},
        function(err) {{
          // Hardware GPS fallback simulation (Sri Lanka coordinates)
          setTimeout(function() {{
            scope.gpsLoading = false;
            scope.gpsAcquired = true;
            scope.gpsCoordinates = "6.9271° N, 79.8612° E (NEO-6M GPS Fix | 8 Sats)";
            scope.gpsStatusText = "GPS 3D Fix Acquired (Accuracy: ±2.5m)";
            scope.setCity("Colombo");
            scope.$applyAsync();
          }}, 800);
        }},
        {{ timeout: 3000 }}
      );
    }} else {{
      setTimeout(function() {{
        scope.gpsLoading = false;
        scope.gpsAcquired = true;
        scope.gpsCoordinates = "6.9271° N, 79.8612° E (NEO-6M GPS Fix | 8 Sats)";
        scope.gpsStatusText = "GPS 3D Fix Acquired (Accuracy: ±2.5m)";
        scope.setCity("Colombo");
        scope.$applyAsync();
      }}, 800);
    }}
  }};

  scope.fetchWeatherPreview = function(city) {{
    fetch('http://localhost:5005/api/weather?city=' + encodeURIComponent(city))
      .then(function(r) {{ return r.json(); }})
      .then(function(d) {{
        scope.weatherPreview = d;
        scope.$applyAsync();
      }})
      .catch(function() {{}});
  }};

  // Submit Registration -> Sync with DynamoDB & Switch to Dashboard
  scope.submitRegistration = function() {{
    if (!scope.regData.plant_name) return;
    scope.isSubmitting = true;

    var payload = {{
      device_id: scope.activeDeviceId,
      plant_name: scope.regData.plant_name,
      scientific_name: scope.regData.scientific_name || (scope.aiPlantProfile ? scope.aiPlantProfile.scientific_name : ''),
      category: scope.regData.category || (scope.aiPlantProfile ? scope.aiPlantProfile.category : 'Botanical Specimen'),
      location_name: scope.regData.location_name,
      min_moisture: scope.regData.min_moisture,
      max_moisture: scope.regData.max_moisture,
      sunlight: scope.regData.sunlight || (scope.aiPlantProfile ? scope.aiPlantProfile.sunlight : ''),
      watering_frequency: scope.regData.watering_frequency || (scope.aiPlantProfile ? scope.aiPlantProfile.watering_frequency : ''),
      notes: scope.regData.notes || (scope.aiPlantProfile ? scope.aiPlantProfile.botanical_summary : '')
    }};

    fetch('http://localhost:5005/api/config', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify(payload)
    }})
    .then(function(res) {{ return res.json(); }})
    .then(function(data) {{
      scope.isSubmitting = false;
      scope.plant = angular.copy(scope.regData);
      if (data && data.weather) scope.weather = data.weather;
      localStorage.setItem('gp_plant_registered', 'true');
      scope.viewMode = 'dashboard';
      scope.evaluateStatus();
      scope.$applyAsync();
    }})
    .catch(function(err) {{
      console.warn("Backend API sync failed, using local registration state:", err);
      scope.isSubmitting = false;
      scope.plant = angular.copy(scope.regData);
      localStorage.setItem('gp_plant_registered', 'true');
      scope.viewMode = 'dashboard';
      scope.evaluateStatus();
      scope.$applyAsync();
    }});
  }};

  // Switch Plant / Relocation Flow
  scope.openRelocationModal = function() {{
    scope.relocationConfirmed = false;
    scope.showRelocationModal = true;
  }};

  scope.closeRelocationModal = function() {{
    scope.showRelocationModal = false;
  }};

  scope.confirmRelocationAndRegister = function() {{
    scope.showRelocationModal = false;
    localStorage.removeItem('gp_plant_registered');
    
    // Call backend unpair
    fetch('http://localhost:5005/api/config/unpair', {{ method: 'POST' }}).catch(function() {{}});

    // Reset telemetry view
    scope.hasReceivedTelemetry = false;
    scope.hardwareConfirmed = false;
    scope.sensor.soil_moisture = null;
    scope.sensor.temperature = null;
    chartHistory.labels = [];
    chartHistory.moisture = [];
    chartHistory.soilTemp = [];
    chartHistory.ambTemp = [];
    chartHistory.humidity = [];
    scope.drawCanvasChart();

    // Switch view back to registration and clear query for fresh AI search
    scope.viewMode = 'register';
    scope.plantSearchQuery = "";
    scope.aiPlantProfile = null;
    scope.$applyAsync();
  }};

  scope.fetchBackendConfig = function() {{
    fetch('http://localhost:5005/api/config')
      .then(function(res) {{ return res.json(); }})
      .then(function(data) {{
        if (data && data.config) {{
          if (data.config.is_registered) {{
            scope.plant = data.config;
            scope.viewMode = 'dashboard';
          }}
          if (data.presets) scope.presets = data.presets;
          scope.refreshWeather();
          scope.$applyAsync();
        }}
      }})
      .catch(function() {{}});
  }};

  scope.refreshWeather = function() {{
    var city = scope.plant.location_name || 'Colombo';
    fetch('http://localhost:5005/api/weather?city=' + encodeURIComponent(city))
      .then(function(res) {{ return res.json(); }})
      .then(function(data) {{
        if (data) {{
          scope.weather = data;
          scope.$applyAsync();
        }}
      }})
      .catch(function() {{}});
  }};

  scope.evaluateStatus = function() {{
    if (!scope.hasReceivedTelemetry || scope.sensor.soil_moisture === null) {{
      scope.aiAdviceHtml = '<div style="color:#64748b; font-style:italic; padding: 25px 0; text-align:center;"><p>Waiting for live sensor data from ESP32 for <strong>' + (scope.plant.plant_name || 'your plant') + '</strong>...</p><small>Once telemetry arrives, click "Run Gemini AI Diagnosis" to analyze plant health.</small></div>';
      return;
    }}
  }};

  scope.runAiDiagnosis = function() {{
    scope.aiLoading = true;
    fetch('http://localhost:5005/api/ai/diagnose', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{
        sensor: scope.sensor,
        plant: scope.plant
      }})
    }})
    .then(function(res) {{ return res.json(); }})
    .then(function(data) {{
      scope.aiLoading = false;
      if (data && data.advice) {{
        var formatted = data.advice.replace(/### (.*?)\\n/g, '<h3>$1</h3>')
                                   .replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>')
                                   .replace(/\\n\\n/g, '<br><br>');
        scope.aiAdviceHtml = formatted;
      }}
      scope.$applyAsync();
    }})
    .catch(function(err) {{
      scope.aiLoading = false;
      scope.aiAdviceHtml = '<p>Unable to connect to Gemini AI Server on port 5005. Please check backend.</p>';
      scope.$applyAsync();
    }});
  }};

  // Watch Node-RED incoming messages
  scope.$watch('msg', function(msg) {{
    if (!msg || !msg.payload) return;
    var p = msg.payload;

    scope.hasReceivedTelemetry = true;
    if (p.temperature !== undefined && p.temperature !== null) scope.sensor.temperature = Number(p.temperature);
    if (p.humidity !== undefined && p.humidity !== null) scope.sensor.humidity = Number(p.humidity);
    if (p.soil_moisture !== undefined && p.soil_moisture !== null) scope.sensor.soil_moisture = Number(p.soil_moisture);
    if (p.soil_temperature !== undefined && p.soil_temperature !== null) scope.sensor.soil_temperature = Number(p.soil_temperature);
    if (p.air_quality_percent !== undefined && p.air_quality_percent !== null) scope.sensor.air_quality_percent = Number(p.air_quality_percent);
    if (p.air_pressure !== undefined && p.air_pressure !== null) scope.sensor.air_pressure = Number(p.air_pressure);
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
    scope.drawCanvasChart();
  }};

  scope.updateChartPoint = function() {{
    if (!scope.hasReceivedTelemetry) return;
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
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;
    for (var y = 20; y < h; y += 40) {{
      ctx.beginPath();
      ctx.moveTo(40, y);
      ctx.lineTo(w - 10, y);
      ctx.stroke();
    }}

    var pts = chartHistory.labels.length;
    if (pts < 2) {{
      ctx.fillStyle = '#94a3b8';
      ctx.font = '600 13px -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Waiting for real-time ESP32 sensor stream...', w / 2, h / 2);
      return;
    }}

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

# Flow definition
flow = [
    {
        "id": "tab_greenpulse",
        "type": "tab",
        "label": "GreenPulse Live Monitor",
        "disabled": False,
        "info": "GreenPulse Plant Onboarding, Relocation & Autonomous Telemetry"
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
        "headers": {
            "Content-Type": "application/json"
        },
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
        temperature: (data.temperature !== undefined && data.temperature !== null) ? Number(data.temperature) : null,
        humidity: (data.humidity !== undefined && data.humidity !== null) ? Number(data.humidity) : null,
        soil_moisture: (data.soil_moisture !== undefined && data.soil_moisture !== null) ? Number(data.soil_moisture) : null,
        soil_temperature: (data.soil_temperature !== undefined && data.soil_temperature !== null) ? Number(data.soil_temperature) : null,
        air_quality_percent: (data.air_quality_percent !== undefined && data.air_quality_percent !== null) ? Number(data.air_quality_percent) : null,
        air_pressure: (data.air_pressure !== undefined && data.air_pressure !== null) ? Number(data.air_pressure) : null,
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
        "id": "ui_full_template",
        "type": "ui_template",
        "z": "tab_greenpulse",
        "group": "ui_group_main",
        "name": "Full-Screen GreenPulse Light UI",
        "order": 1,
        "width": "24",
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
