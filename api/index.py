from app import create_app

app = create_app()

# Vercel serverless function handler (если требуется)
def handler(request, context):
    return app(request, context) 