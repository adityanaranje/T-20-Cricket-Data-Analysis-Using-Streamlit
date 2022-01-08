mkdir -p ~/.streamlit/

echo "[theme]
primaryColor="#13fbe6"
backgroundColor="#080808"
secondaryBackgroundColor="#22222d"
textColor="#fffefe"
font="serif"
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml