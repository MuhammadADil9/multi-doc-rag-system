from app.database.connection import init_db

if __name__ == "__main__":
    print("=" * 50)
    print("INITIALIZING DATABASE")
    print("=" * 50)

    try:
        init_db()
        print("=" * 50)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback

        traceback.print_exc()
