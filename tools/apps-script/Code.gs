/**
 * Lightbox Digital — analytics proxy for the studio dashboard.
 *
 * Runs inside the Google account that owns the Analytics property, so no
 * Cloud project or OAuth client is needed. Deployed as a web app, it returns
 * the dashboard's six reports as JSON.
 *
 * SETUP
 *  1. script.google.com → New project → paste this file over Code.gs
 *  2. Fill in PROPERTY_ID and SHARED_KEY below
 *  3. Project Settings → tick "Show appsscript.json manifest file",
 *     then paste the appsscript.json from this folder over it
 *  4. Deploy → New deployment → Web app
 *       Execute as:      Me
 *       Who has access:  Anyone
 *     Authorise when prompted (it asks to read Analytics — that is this script)
 *  5. Copy the web app URL and paste it into the dashboard as:
 *       <that url>?key=<your SHARED_KEY>
 */

var PROPERTY_ID = 'REPLACE_WITH_PROPERTY_ID';   // Analytics ▸ Admin ▸ Property settings (a number)
var SHARED_KEY  = 'REPLACE_WITH_A_RANDOM_KEY';  // any random string; must match the ?key= in the URL

function doGet(e) {
  var key = (e && e.parameter && e.parameter.key) || '';
  if (key !== SHARED_KEY) return json_({ error: 'unauthorized' });
  try {
    return json_({ reports: fetchAll_(), generated: new Date().toISOString() });
  } catch (err) {
    return json_({ error: String(err) });
  }
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function api_(method, body) {
  var res = UrlFetchApp.fetch(
    'https://analyticsdata.googleapis.com/v1beta/properties/' + PROPERTY_ID + ':' + method, {
      method: 'post',
      contentType: 'application/json',
      headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() },
      payload: JSON.stringify(body),
      muteHttpExceptions: true
    });
  if (res.getResponseCode() !== 200) {
    throw new Error('Analytics API ' + res.getResponseCode() + ': ' + res.getContentText().slice(0, 300));
  }
  return JSON.parse(res.getContentText());
}

function fetchAll_() {
  var M = function (names) { return names.map(function (n) { return { name: n }; }); };
  var RANGE = [{ startDate: '28daysAgo', endDate: 'today' }];
  return [
    api_('runReport', { dateRanges: RANGE,
      metrics: M(['activeUsers', 'newUsers', 'sessions', 'screenPageViews', 'bounceRate', 'averageSessionDuration']) }),
    api_('runReport', { dateRanges: RANGE, dimensions: M(['date']), metrics: M(['activeUsers']),
      orderBys: [{ dimension: { dimensionName: 'date' } }] }),
    api_('runReport', { dateRanges: RANGE, dimensions: M(['pagePath']), metrics: M(['screenPageViews', 'bounceRate']),
      limit: 10, orderBys: [{ metric: { metricName: 'screenPageViews' }, desc: true }] }),
    api_('runReport', { dateRanges: RANGE, dimensions: M(['sessionDefaultChannelGroup']), metrics: M(['sessions']),
      limit: 8, orderBys: [{ metric: { metricName: 'sessions' }, desc: true }] }),
    api_('runReport', { dateRanges: RANGE, dimensions: M(['eventName']), metrics: M(['eventCount']),
      limit: 15, orderBys: [{ metric: { metricName: 'eventCount' }, desc: true }] }),
    api_('runRealtimeReport', { metrics: M(['activeUsers']) })
  ];
}

/** Run this once from the editor to check the setup before deploying. */
function testConnection() {
  var r = fetchAll_()[0];
  Logger.log('Visitors in the last 28 days: ' + r.rows[0].metricValues[0].value);
}
