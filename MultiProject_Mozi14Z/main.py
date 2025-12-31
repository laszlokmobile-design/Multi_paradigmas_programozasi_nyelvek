#main.py
import subprocess
import sys
import os
import threading


BASE_DIR = os.path.dirname(os.path.abspath(__file__))



def start_backend():
    try:
        print("🚀 FastAPI backend indítása...")
        # 1️⃣ DB feltöltése, ha üres
        import backend.seed
        backend.seed.populate_db()  # ez feltölti az adatbázist


        return subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload"
        ])
    except Exception as e:
        print(f"❌ Hiba a backend indításakor: {e}")
        return None

def start_frontend():
    print("🎬 Streamlit frontend indítása...")
    return subprocess.Popen(["streamlit", "run", "frontend/app.py"])

def start_docker():
    print("🐳 Docker Compose indítása...")
    return subprocess.Popen(
        ["docker", "compose", "up", "--build"],
        cwd = BASE_DIR
    )

def main():
    print("""
🎞️ Mozi / Filmajánló rendszer
Válassz egy opciót:
1 - Csak backend3
2 - Csak frontend
3 - Backend + frontend
4 - Docker Compose
""")
    choice = input("➡️ Választás: ")

    processes = []

    if choice in ["1", "3"]:  # backend-only vagy backend+frontend
        import backend.email_scheduler as email_scheduler
        scheduler_thread = threading.Thread(target=email_scheduler.run_scheduler, daemon=True)
        scheduler_thread.start()

    if choice == "1":
        processes.append(start_backend())
    elif choice == "2":
        processes.append(start_frontend())
    elif choice == "3":
        processes.append(start_backend())
        processes.append(start_frontend())
    elif choice == "4":
        processes.append(start_docker())
    else:
        print("❌ Érvénytelen választás.")
        return

    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\n🛑 Leállítás...")
        for p in processes:
            p.terminate()

if __name__ == "__main__":
    main()

