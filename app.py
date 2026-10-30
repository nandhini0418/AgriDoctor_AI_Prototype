"""
app.py
------
AgriDoctor AI -- Streamlit prototype.

Run with:
    streamlit run app.py
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

import database as db
import model as ai
import weather
from i18n import t, t_severity, t_crop, t_disease_name, localize_disease_info, translate_disease_name, LANGUAGES, TTS_LANG_CODE

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="AgriDoctor AI",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

NAVY = "#0E2841"
ORANGE = "#E97132"
LEAF = "#2F6D3A"
RUST = "#C1432A"
AMBER = "#C98A00"

# Severity -> colour, used for the result card's accent border and badge.
# Keys are always the English severity word from the database, regardless
# of display language, so this mapping never needs translating.
SEVERITY_COLORS = {
    "none": LEAF,
    "mild": AMBER,
    "moderate": ORANGE,
    "severe": RUST,
}


def severity_color(severity: str) -> str:
    key = (severity or "none").strip().lower()
    if key in ("", "nan"):
        key = "none"
    return SEVERITY_COLORS.get(key, ORANGE)


# ---------------------------------------------------------------------------
# Setup (runs once per session)
# ---------------------------------------------------------------------------
@st.cache_resource
def setup():
    db.init_db()
    return True


setup()

# ---------------------------------------------------------------------------
# Voice-selected crop bridge: the sidebar's "Say your crop name" button (see
# below) uses the browser's speech recognition, then reloads the page with
# ?crop=... in the URL so Python can pick it up here, since a Streamlit
# components.html iframe can't set Python state directly.
# ---------------------------------------------------------------------------
CROP_OPTIONS = ["Tomato", "Potato", "Corn"]
_voice_crop = st.query_params.get("crop")
_default_crop_index = CROP_OPTIONS.index(_voice_crop) if _voice_crop in CROP_OPTIONS else 0
if _voice_crop in CROP_OPTIONS:
    st.query_params.clear()  # consume it so a manual dropdown change isn't overridden later

if "lang" not in st.session_state:
    st.session_state["lang"] = "en"
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "otp_sent" not in st.session_state:
    st.session_state["otp_sent"] = False


def render_login():
    """A simple prototype login gate, matching the pitch deck's login mockup.
    No real authentication or SMS -- any 4-digit code is accepted, and
    "Continue as Guest" skips straight in. This exists to demonstrate the
    UX flow, not to secure anything."""
    lang = st.session_state["lang"]

    top_l, top_r = st.columns([3, 1])
    with top_r:
        lang_choice = st.selectbox(
            t("language_label", lang), options=list(LANGUAGES.keys()),
            format_func=lambda code: LANGUAGES[code],
            index=list(LANGUAGES.keys()).index(lang), key="login_lang",
        )
        st.session_state["lang"] = lang_choice
        lang = lang_choice

    st.markdown(
        f"""
        <div style="background:linear-gradient(160deg,{NAVY},#156082); padding:40px 34px;
                    border-radius:18px; color:white; max-width:460px; margin:10px auto 0 auto;">
            <div style="font-size:26px; font-weight:700;">🌿 {t('app_title', lang)}</div>
            <div style="font-size:13.5px; opacity:0.85; margin-top:8px;">{t('login_welcome', lang)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if not st.session_state["otp_sent"]:
            name = st.text_input(t("login_name_label", lang), key="login_name_input")
            phone = st.text_input(t("login_phone_label", lang), key="login_phone_input")
            if st.button(t("login_send_otp", lang), type="primary", use_container_width=True):
                if not name.strip():
                    st.warning(t("login_please_enter_name", lang))
                elif not phone.strip():
                    st.warning(t("login_please_enter_phone", lang))
                else:
                    st.session_state["otp_sent"] = True
                    st.session_state["pending_name"] = name.strip()
                    st.rerun()
            st.caption(t("login_or", lang))
            if st.button(t("login_guest", lang), use_container_width=True):
                st.session_state["logged_in"] = True
                st.session_state["user_name"] = t("guest_name", lang)
                st.rerun()
        else:
            st.info(t("login_otp_hint", lang), icon="🔑")
            otp = st.text_input(t("login_otp_label", lang), max_chars=4, key="login_otp_input")
            if st.button(t("login_verify_button", lang), type="primary", use_container_width=True):
                if otp.strip().isdigit() and len(otp.strip()) == 4:
                    st.session_state["logged_in"] = True
                    st.session_state["user_name"] = st.session_state.get("pending_name", "")
                    st.rerun()
                else:
                    st.warning(t("login_invalid_otp", lang))


if not st.session_state["logged_in"]:
    render_login()
    st.stop()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(f"<h2 style='color:{NAVY};'>🌿 {t('app_title', st.session_state['lang'])}</h2>", unsafe_allow_html=True)
    st.caption(t("tagline", st.session_state["lang"]))
    st.divider()

    lang_label = st.selectbox(
        t("language_label", st.session_state["lang"]),
        options=list(LANGUAGES.keys()),
        format_func=lambda code: LANGUAGES[code],
        index=list(LANGUAGES.keys()).index(st.session_state["lang"]),
    )
    st.session_state["lang"] = lang_label
    lang = st.session_state["lang"]

    st.caption(f"{t('logged_in_as', lang)}: **{st.session_state['user_name']}**")
    if st.button(t("logout_button", lang), use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["otp_sent"] = False
        st.session_state["user_name"] = ""
        st.rerun()

    st.divider()
    page = st.radio(
        t("navigate_label", lang),
        [t("nav_scan", lang), t("nav_reports", lang), t("nav_notifications", lang), t("nav_about", lang)],
    )

    st.divider()
    crop = st.selectbox(
        t("crop_label", lang), CROP_OPTIONS, index=_default_crop_index,
        format_func=lambda c: t_crop(c, lang),
    )

    # Voice input: speak a crop name instead of using the dropdown. Works in
    # Chrome-based browsers (Web Speech API); other browsers show a message
    # instead of failing silently.
    components.html(
        f"""
        <div>
          <button id="voicebtn" style="width:100%; padding:9px; border-radius:20px; border:1.4px solid {NAVY};
                background:white; color:{NAVY}; font-weight:700; font-size:13px; cursor:pointer;">
            {t('voice_crop_button', lang)}
          </button>
          <div id="voicestatus" style="font-size:11px; color:#6C7B83; margin-top:6px;"></div>
        </div>
        <script>
        const btn = document.getElementById('voicebtn');
        const status = document.getElementById('voicestatus');
        btn.onclick = function() {{
          const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
          if (!SpeechRecognition) {{
            status.innerText = {json.dumps(t('voice_no_support', lang))};
            return;
          }}
          const recognition = new SpeechRecognition();
          recognition.lang = "{TTS_LANG_CODE.get(lang, 'en-IN')}";
          recognition.interimResults = false;
          status.innerText = {json.dumps(t('voice_listening', lang))};
          recognition.start();
          recognition.onresult = function(event) {{
            const text = event.results[0][0].transcript.toLowerCase();
            let matched = null;
            if (text.includes("tomato") || text.includes("thakkali") || text.includes("takkali") || text.includes("tamatar")) matched = "Tomato";
            else if (text.includes("potato") || text.includes("urulai") || text.includes("aloo") || text.includes("alu")) matched = "Potato";
            else if (text.includes("corn") || text.includes("maize") || text.includes("solam") || text.includes("makka")) matched = "Corn";
            if (matched) {{
              status.innerText = "\\"" + text + "\\" -> " + matched;
              const url = new URL(window.parent.location.href);
              url.searchParams.set("crop", matched);
              window.parent.location.href = url.toString();
            }} else {{
              status.innerText = {json.dumps(t('voice_no_match', lang))} + " \\"" + text + "\\"";
            }}
          }};
          recognition.onerror = function(event) {{
            status.innerText = {json.dumps(t('voice_error', lang))} + " " + event.error;
          }};
        }};
        </script>
        """,
        height=70,
    )

    st.divider()
    model_loaded = ai.load_trained_model()
    if model_loaded is None:
        st.warning(t("demo_mode_warning", lang), icon="⚠️")
    else:
        st.success(t("trained_mode_success", lang), icon="✅")

    st.divider()
    with st.expander(t("weather_expander", lang)):
        city = st.text_input(t("city_label", lang), value="Chennai", key="weather_city")
        if st.button(t("check_forecast_button", lang)):
            with st.spinner("..."):
                advice = weather.get_rain_advice(city)
            st.session_state["last_weather"] = advice
            st.session_state["last_weather_city"] = city
            if advice.get("available"):
                if advice["should_delay_spraying"]:
                    st.warning(
                        "🌧️ " + t("weather_delay", lang, city=advice["location"], pct=advice["max_rain_chance"])
                    )
                else:
                    st.success(
                        "🌤️ " + t("weather_ok", lang, city=advice["location"], pct=advice["max_rain_chance"])
                    )
            elif advice.get("error") == "city_not_found":
                st.info(t("weather_city_not_found", lang, city=city))
            elif advice.get("error") == "forecast_failed":
                st.info(t("weather_forecast_failed", lang, city=advice.get("location", city)))
            else:
                st.info(t("weather_unavailable", lang))


# ---------------------------------------------------------------------------
# Page: Scan a Leaf
# ---------------------------------------------------------------------------
if page == t("nav_scan", lang):
    st.markdown(f"<h1 style='color:{NAVY};'>{t('scan_heading', lang)}</h1>", unsafe_allow_html=True)
    st.caption(t("scan_caption", lang))

    col1, col2 = st.columns(2)
    with col1:
        source_choice = st.radio(
            t("image_source_label", lang),
            [t("upload_option", lang), t("camera_option", lang)],
            horizontal=True,
        )
        image_file = None
        source_tag = "upload"

        if source_choice == t("upload_option", lang):
            image_file = st.file_uploader(t("choose_image_label", lang), type=["jpg", "jpeg", "png"])
        else:
            image_file = st.camera_input(t("camera_input_label", lang))
            source_tag = "camera"

        analyze_clicked = False
        if image_file is not None:
            st.image(image_file, caption=t("selected_image_caption", lang), use_container_width=True)
            analyze_clicked = st.button(t("analyze_button", lang), type="primary", use_container_width=True)

    with col2:
        if image_file is not None and analyze_clicked:
            pil_image = Image.open(image_file)
            with st.spinner(t("analyzing_spinner", lang)):
                class_name, confidence, mode = ai.predict(pil_image, crop=crop)
                info = db.get_disease_info(class_name)  # English, used for logging/comparison

            new_id = db.log_scan(
                crop=info["crop"],
                class_name=class_name,
                disease=info["disease"],
                confidence=confidence,
                source=source_tag,
            )

            display = localize_disease_info(class_name, info, lang)  # translated, for display only
            sev_color = severity_color(info["severity"])

            st.markdown(
                f"""
                <div style="background:{NAVY}; padding:22px 26px; border-radius:14px; color:white;
                            border-left:7px solid {sev_color};">
                    <div style="font-size:12px; opacity:0.75;">{display['crop']} · {t('analyzed_now', lang)}
                        {' · ' + t('demo_mode_tag', lang) if mode == 'demo' else ''}</div>
                    <div style="font-size:24px; font-weight:700; margin-top:6px;">{display['crop']} — {display['disease']}</div>
                    <div style="margin-top:12px; display:flex; align-items:center; gap:10px;">
                        <div style="flex:1; background:rgba(255,255,255,0.18); border-radius:6px; height:8px;">
                            <div style="width:{confidence*100:.0f}%; background:{ORANGE}; height:8px; border-radius:6px;"></div>
                        </div>
                        <div style="font-weight:700;">{confidence*100:.0f}%</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<span style='background:{sev_color}22; color:{sev_color}; padding:4px 10px; "
                f"border-radius:10px; font-size:12px; font-weight:700;'>{t('severity_prefix', lang)}: {display['severity_label']}</span>",
                unsafe_allow_html=True,
            )

            # -- Compare with last scan for this crop (compared in English,
            #    displayed translated) --
            previous = db.get_previous_scan(info["crop"], before_id=new_id)
            if previous:
                prev_disease = previous["disease"]
                prev_conf = previous["confidence"]
                was_healthy = prev_disease.lower() == "healthy"
                is_healthy_now = info["disease"].lower() == "healthy"
                prev_disease_display = translate_disease_name(previous.get("class_name"), lang, prev_disease)

                if prev_disease.lower() == info["disease"].lower():
                    delta = (confidence - prev_conf) * 100
                    direction = t("compare_up", lang) if delta > 0 else (t("compare_down", lang) if delta < 0 else t("compare_unchanged", lang))
                    st.caption(
                        t("compare_same", lang, crop=display["crop"], disease=display["disease"],
                          direction=direction, delta=f"{abs(delta):.0f}", date=previous["timestamp"][:10])
                    )
                elif is_healthy_now and not was_healthy:
                    st.success(t("compare_improved", lang, date=previous["timestamp"][:10], prev=prev_disease_display), icon="📈")
                elif was_healthy and not is_healthy_now:
                    st.warning(t("compare_worsened", lang, date=previous["timestamp"][:10], curr=display["disease"]), icon="📉")
                else:
                    st.caption(
                        t("compare_other", lang, crop=display["crop"], date=previous["timestamp"][:10],
                          prev=prev_disease_display, pct=f"{prev_conf*100:.0f}")
                    )

            st.markdown(f"#### {t('about_heading', lang)}")
            st.write(display["description"])

            st.markdown(f"#### {t('treatment_heading', lang)}")
            for i, step in enumerate(display["remedy"].split(". "), start=1):
                step = step.strip().rstrip(".")
                if step:
                    st.markdown(f"**{i}.** {step}.")

            # -- Voice output: read the diagnosis aloud, in the selected language --
            tts_text = (
                f"{display['crop']}. {display['disease']}. {confidence*100:.0f}%. "
                f"{display['description']} {display['remedy']}"
            )
            components.html(
                f"""
                <button id="ttsbtn" style="padding:10px 16px; border-radius:20px; border:none;
                        background:{ORANGE}; color:white; font-weight:700; font-size:13px; cursor:pointer;">
                  {t('listen_button', lang)}
                </button>
                <script>
                document.getElementById('ttsbtn').onclick = function() {{
                  if (!window.speechSynthesis) {{ return; }}
                  window.speechSynthesis.cancel();
                  const utter = new SpeechSynthesisUtterance({json.dumps(tts_text)});
                  utter.lang = "{TTS_LANG_CODE.get(lang, 'en-IN')}";
                  window.speechSynthesis.speak(utter);
                }};
                </script>
                """,
                height=55,
            )

            st.success(t("saved_message", lang), icon="💾")
        else:
            st.info(t("scan_placeholder", lang))


# ---------------------------------------------------------------------------
# Page: Reports & History
# ---------------------------------------------------------------------------
elif page == t("nav_reports", lang):
    st.markdown(f"<h1 style='color:{NAVY};'>{t('reports_heading', lang)}</h1>", unsafe_allow_html=True)

    history = db.fetch_history()

    if history.empty:
        st.info(t("no_scans_yet", lang))
    else:
        total_scans = len(history)
        issues_found = int((history["disease"].str.lower() != "healthy").sum())
        avg_conf = history["confidence"].mean() * 100

        c1, c2, c3 = st.columns(3)
        c1.metric(t("metric_scans_done", lang), total_scans)
        c2.metric(t("metric_issues_found", lang), issues_found)
        c3.metric(t("metric_avg_confidence", lang), f"{avg_conf:.0f}%")

        st.markdown(f"#### {t('scans_over_time', lang)}")
        ts = history.copy()
        ts["timestamp"] = pd.to_datetime(ts["timestamp"])
        ts = ts.sort_values("timestamp")
        st.line_chart(ts.set_index("timestamp")["confidence"])

        st.markdown(f"#### {t('most_common_issues', lang)}")
        freq = history[history["disease"].str.lower() != "healthy"]["disease"].value_counts()
        if not freq.empty:
            freq_display = freq.copy()
            freq_display.index = [t_disease_name(name, lang) for name in freq_display.index]
            st.bar_chart(freq_display)
        else:
            st.caption(t("no_issues_yet", lang))

        st.markdown(f"#### {t('full_history', lang)}")
        history_display = history.copy()
        history_display["crop"] = history_display["crop"].apply(lambda c: t_crop(c, lang))
        history_display["disease"] = history_display.apply(
            lambda r: translate_disease_name(r["class_name"], lang, r["disease"]), axis=1
        )
        st.dataframe(
            history_display[["timestamp", "crop", "disease", "confidence", "source"]],
            use_container_width=True,
            hide_index=True,
        )
        st.download_button(
            t("download_csv_button", lang),
            data=history.to_csv(index=False).encode("utf-8"),
            file_name="agridoctor_scan_history.csv",
            mime="text/csv",
        )

        st.markdown(f"#### {t('manage_entries', lang)}")
        st.caption(t("manage_entries_caption", lang))
        recent = history.head(20)
        options = {
            f"#{row.id} — {row.timestamp[:16]} — {t_crop(row.crop, lang)} — "
            f"{translate_disease_name(row.class_name, lang, row.disease)} ({row.confidence*100:.0f}%)": row.id
            for row in recent.itertuples()
        }
        if options:
            choice = st.selectbox(t("select_entry_label", lang), list(options.keys()))
            if st.button(t("delete_entry_button", lang)):
                db.delete_scan(options[choice])
                st.rerun()

        with st.expander(t("reset_all_expander", lang)):
            st.caption(t("reset_all_caption", lang))
            if st.button(t("clear_all_button", lang)):
                db.clear_history()
                st.rerun()


# ---------------------------------------------------------------------------
# Page: Notifications
# ---------------------------------------------------------------------------
elif page == t("nav_notifications", lang):
    st.markdown(f"<h1 style='color:{NAVY};'>{t('notifications_heading', lang)}</h1>", unsafe_allow_html=True)

    history = db.fetch_history()
    today_str = datetime.now().strftime("%Y-%m-%d")

    cards = []  # list of (timestamp_str, is_today, kind, title, body, show_rescan)

    if not history.empty:
        latest_per_crop = history.sort_values("timestamp").groupby("crop", as_index=False).tail(1)
        for row in latest_per_crop.itertuples():
            date_str = row.timestamp[:10]
            is_today = date_str == today_str
            crop_name = t_crop(row.crop, lang)
            if row.disease.lower() != "healthy":
                disease_name = translate_disease_name(row.class_name, lang, row.disease)
                cards.append((
                    row.timestamp, is_today, "warning",
                    t("notif_recheck_title", lang, crop=crop_name),
                    t("notif_recheck_sub", lang, date=date_str, disease=disease_name),
                    True,
                ))
            else:
                cards.append((
                    row.timestamp, is_today, "success",
                    t("notif_healthy_title", lang, crop=crop_name),
                    t("notif_healthy_sub", lang, date=date_str),
                    False,
                ))

    # Opportunistic weather notification, from the sidebar's last check.
    last_weather = st.session_state.get("last_weather")
    if last_weather and last_weather.get("available") and last_weather.get("should_delay_spraying"):
        cards.append((
            datetime.now().isoformat(timespec="seconds"), True, "warning",
            t("notif_weather_title", lang, city=last_weather["location"]),
            t("notif_weather_sub", lang, pct=last_weather["max_rain_chance"]),
            False,
        ))

    # Always-present tip, shown under "Earlier".
    cards.append(("", False, "info", t("notif_tip_title", lang), t("notif_tip_sub", lang), False))

    if not history.empty or last_weather:
        cards.sort(key=lambda c: c[0], reverse=True)

        today_cards = [c for c in cards if c[1]]
        earlier_cards = [c for c in cards if not c[1]]

        def render_card(kind, title, body, show_rescan):
            icon = {"warning": "⚠️", "success": "✅", "info": "💡"}[kind]
            box = {"warning": st.warning, "success": st.success, "info": st.info}[kind]
            box(f"**{title}**\n\n{body}", icon=icon)
            if show_rescan:
                st.caption(f"👉 {t('notif_rescan_button', lang)}: {t('nav_scan', lang)}")

        if today_cards:
            st.markdown(f"#### {t('group_today', lang)}")
            for _, _, kind, title, body, show_rescan in today_cards:
                render_card(kind, title, body, show_rescan)

        if earlier_cards:
            st.markdown(f"#### {t('group_earlier', lang)}")
            for _, _, kind, title, body, show_rescan in earlier_cards:
                render_card(kind, title, body, show_rescan)
    else:
        st.info(t("notif_none_yet", lang))


# ---------------------------------------------------------------------------
# Page: About
# ---------------------------------------------------------------------------
else:
    st.markdown(f"<h1 style='color:{NAVY};'>{t('about_title', lang)}</h1>", unsafe_allow_html=True)
    st.write(t("about_intro", lang))

    st.markdown(f"#### {t('how_it_works_heading', lang)}")
    st.markdown(t("how_it_works_steps", lang))

    st.markdown(f"#### {t('tech_stack_heading', lang)}")
    st.markdown(
        """
        | Layer      | Technology                                   |
        |------------|-----------------------------------------------|
        | Front end  | Streamlit (Python-based UI)                    |
        | Back end   | Python                                         |
        | Database   | SQLite (disease & remedy lookup, scan history) |
        | AI / ML    | TensorFlow, Keras, MobileNetV2 (transfer learning) |
        | Weather    | Open-Meteo (free, no API key)                  |
        | Voice      | Browser Web Speech API (input + output)        |
        | Hardware   | Smartphone camera (image capture)              |
        """
    )

    st.caption(f"{t('built_for_caption', lang)} {datetime.now().strftime('%Y-%m-%d %H:%M')}")
