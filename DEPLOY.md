# How to Deploy to Vercel

## Option 1: Deploy via GitHub (Recommended)

1.  **Push your changes** to your GitHub repository.
    ```bash
    git add .
    git commit -m "Prepare poster for deployment"
    git push origin main
    ```

2.  **Go to Vercel Dashboard** (https://vercel.com/dashboard).

3.  **Add New Project**:
    *   Click "Add New..." -> "Project".
    *   Import your repository (`load--forcasting-nama-`).

4.  **Configure Project**:
    *   **Framework Preset**: Other (or leave as default).
    *   **Root Directory**: Click "Edit" and select `web-poster`.
        *   *Note: Since your repo root is `C:/Users/ahmed/Desktop/11kv hembar/detailed/Al Humbar PSS Load Details`, and the poster is in `web-poster`, you should set the Root Directory to `web-poster`.*

5.  **Deploy**: Click "Deploy".

## Option 2: Deploy via Vercel CLI

1.  **Install Vercel CLI** (if not installed):
    ```bash
    npm i -g vercel
    ```

2.  **Login**:
    ```bash
    vercel login
    ```

3.  **Deploy**:
    Run the following command inside the `web-poster` directory:
    ```bash
    cd web-poster
    vercel
    ```
    *   Follow the prompts (Set up and deploy? [Y], Link to existing project? [N], etc.).
