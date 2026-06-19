FROM ghcr.io/prefix-dev/pixi:0.66.0

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860

COPY pyproject.toml pixi.lock ./
RUN pixi install --environment default

COPY dash_app ./dash_app
COPY models ./models
COPY outputs ./outputs
COPY VERSION VERSION.md ./

EXPOSE 7860
CMD ["pixi", "run", "dash-prod"]
