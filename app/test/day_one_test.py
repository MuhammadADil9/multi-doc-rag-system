from app.services.pdf_parser import PDFParser
from app.services.text_splitter import TextSplitterService
from app.config import settings


def test_pdf_pipeline():
    """Test PDF → Text → Chunks pipeline"""

    # Step 1: Validate & Parse PDF
    pdf_path = "app/battle_of_hattin.pdf"

    print("=" * 50)
    print("STEP 1: Validating PDF")
    print("=" * 50)

    try:
        PDFParser.validate_file(pdf_path, settings.MAX_FILE_SIZE_MB)
        print("✓ Validation passed")
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return

    print("\n" + "=" * 50)
    print("STEP 2: Extracting Text")
    print("=" * 50)

    try:
        text = PDFParser.extract_text(pdf_path)
        print(f"✓ Extracted {len(text)} characters")
        print(f"Preview: {text[:200]}...")
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return

    print("\n" + "=" * 50)
    print("STEP 3: Splitting into Chunks")
    print("=" * 50)

    try:
        splitter = TextSplitterService()
        chunks = splitter.split_text(text)
        print(f"✓ Created {len(chunks)} chunks")
        print(f"\nFirst chunk ({len(chunks[0])} chars):")
        print(chunks[0])
        print(f"\nLast chunk ({len(chunks[-1])} chars):")
        print(chunks[-1])
    except Exception as e:
        print(f"✗ Splitting failed: {e}")
        return

    print("\n" + "=" * 50)
    print("✓ DAY 1 PIPELINE COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    test_pdf_pipeline()
