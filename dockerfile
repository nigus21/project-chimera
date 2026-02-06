FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir pytest flake8 bandit black

# Add non-root user for security
RUN useradd -m chimera
USER chimera

# Copy code
COPY . .

# Default command runs lint + tests
CMD ["bash", "-c", "flake8 . && black --check . && bandit -r . && pytest"]