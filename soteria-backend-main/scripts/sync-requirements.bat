poetry export -f requirements.txt --without-hashes -o requirements.txt >nul 2>&1 ^
&& poetry export -f requirements.txt --without-hashes --dev -o requirements-dev.txt >nul 2>&1
