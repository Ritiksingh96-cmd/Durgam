import os, shutil

static_dir = os.path.join('backend', 'app', 'static')
root_dir = '.'

# Files to keep strictly in sync
extensions = ('.html', '.css', '.js')

# Copy newer files between root and static_dir
for f in os.listdir(root_dir):
    if f.endswith(extensions):
        root_path = os.path.join(root_dir, f)
        static_path = os.path.join(static_dir, f)
        if os.path.isfile(root_path):
            shutil.copy2(root_path, static_path)

print('Synchronized all root and backend/app/static files successfully.')

