mkdir -p ~/.streamlit

echo "[theme]
base="light"
backgroundColor="#f5f4f2"
secondaryBackgroundColor="#e3f2fc"
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml