// In-browser voice demo using the Web Speech API.
// Zero backend, zero API key: audio is synthesized on the visitor's device.
(function () {
  const root = document.querySelector('[data-tts]');
  if (!root) return;

  const els = {
    lang: root.querySelector('#tts-lang'),
    voice: root.querySelector('#tts-voice'),
    rate: root.querySelector('#tts-rate'),
    text: root.querySelector('#tts-text'),
    speak: root.querySelector('#tts-speak'),
    stop: root.querySelector('#tts-stop'),
    status: root.querySelector('#tts-status'),
    unsupported: root.querySelector('#tts-unsupported'),
  };

  const SCRIPTS = {
    'en-US': "Hi, I am Otman's AI deployment assistant. I can explain his readiness audits, implementation sprints, and training work. For a real project, start with one painful workflow and one measurable outcome.",
    'fr-FR': "Bonjour, je suis l'assistant de déploiement IA d'Otman. Je peux expliquer ses audits de préparation, ses sprints d'implémentation et ses formations. Pour un vrai projet, commencez par un flux pénible et un résultat mesurable.",
    'es-ES': "Hola, soy el asistente de despliegue de IA de Otman. Puedo explicar sus auditorías de preparación, sus sprints de implementación y su formación. Para un proyecto real, empiece por un flujo doloroso y un resultado medible.",
  };

  const supported = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
  const setStatus = (s) => { if (els.status) els.status.textContent = s; };
  const currentLang = () => (els.lang ? els.lang.value : 'en-US');

  if (!supported) {
    if (els.unsupported) els.unsupported.hidden = false;
    [els.speak, els.stop, els.lang, els.voice, els.rate].forEach((e) => { if (e) e.disabled = true; });
    setStatus('In-browser speech is unavailable here — use the neural version below.');
    return;
  }

  const synth = window.speechSynthesis;
  let voices = [];

  function matchingVoices(lang) {
    const base = (lang || 'en').split('-')[0].toLowerCase();
    const m = voices.filter((v) => v.lang && v.lang.toLowerCase().startsWith(base));
    return m.length ? m : voices;
  }

  function populateVoices() {
    if (!els.voice) return;
    const list = matchingVoices(currentLang());
    els.voice.innerHTML = '';
    if (!list.length) {
      const opt = document.createElement('option');
      opt.value = '';
      opt.textContent = 'Default browser voice';
      els.voice.appendChild(opt);
      return;
    }
    list.forEach((v) => {
      const opt = document.createElement('option');
      opt.value = v.name;
      opt.textContent = v.name + ' (' + v.lang + ')';
      els.voice.appendChild(opt);
    });
  }

  function loadVoices() {
    voices = synth.getVoices() || [];
    populateVoices();
  }

  loadVoices();
  // Voices often load asynchronously; refresh when they arrive.
  if (typeof synth.onvoiceschanged !== 'undefined') {
    synth.onvoiceschanged = loadVoices;
  }

  function toggle(speaking) {
    if (els.speak) els.speak.disabled = speaking;
    if (els.stop) els.stop.disabled = !speaking;
  }

  function speak() {
    const text = ((els.text && els.text.value) || '').trim();
    if (!text) { setStatus('Type a short script first.'); return; }
    synth.cancel();
    const u = new SpeechSynthesisUtterance(text.slice(0, 600));
    u.lang = currentLang();
    if (els.rate) u.rate = parseFloat(els.rate.value) || 1;
    const chosen = els.voice && els.voice.value;
    const v = voices.find((x) => x.name === chosen);
    if (v) u.voice = v;
    u.onstart = () => { setStatus('Speaking…'); toggle(true); };
    u.onend = () => { setStatus('Done.'); toggle(false); };
    u.onerror = (e) => { setStatus('Could not speak: ' + (e.error || 'unknown')); toggle(false); };
    synth.speak(u);
  }

  function stop() {
    synth.cancel();
    setStatus('Stopped.');
    toggle(false);
  }

  if (els.lang) {
    els.lang.addEventListener('change', () => {
      populateVoices();
      if (els.text && SCRIPTS[currentLang()]) els.text.value = SCRIPTS[currentLang()];
    });
  }
  if (els.speak) els.speak.addEventListener('click', speak);
  if (els.stop) els.stop.addEventListener('click', stop);
  // Stop speech if the visitor navigates away.
  window.addEventListener('beforeunload', () => synth.cancel());

  toggle(false);
})();
