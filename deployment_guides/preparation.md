# Preparing Your Project for Deployment

## 1. Update Flask App to Serve Static Files

Update your app.py to serve the React frontend in production:

```python
# Add to app.py
import os

# Serve React frontend in production
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
```

## 2. Create a requirements.txt with Deployment Dependencies

Add these to your requirements.txt:
