import warnings
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import re





def search_verse(version, reference):
    # Because we are using an html parser for an xml file, we need to suppress the warnings against it (because it works)
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)


    # Mapping versions to corresponding XML files
    versionToXML = {
        "ESV": 'Bible_English_ESV.xml',
        "NKJV": "Bible_English_NKJV.xml",
        "NLT": "Bible_English_NLT.xml",
        "RV09": "Bible_Espanol_RV09.xml"
    }

    # Get the correct XML file based on the version
    xml_file = versionToXML.get(version)
    if not xml_file:
        return f"Version '{version}' not found.", f"Version '{version}' not found."
    
    # Read and clean the XML file
    with open(xml_file, 'r', encoding='utf-8') as f:
        data = re.sub(r'xmlns(:\w+)?="[^"]+"', '', f.read(), count=1)
    
    # Your XML parsing code
    Bs_data = BeautifulSoup(data, "html.parser")
    
    # Regex for scripture reference input (book name, chapter, and verse(s))
    match = re.match(r"^\s*(\d?\s*\w+)\s*(\d{1,3}(?:-\d{1,3})?)\s*(?::(\d{1,3}(?:-\d{1,3})?)?)?\s*$", reference)
    
    if match:
        # Convert input to lowercase for case-insensitive comparison
        bk, chpt, vs = match.group(1).strip().lower(), match.group(2).strip(), match.group(3).strip() if match.group(3) else ''
        
        result = []
        try:
            # Find book using lowercase comparison (case-insensitive search)
            book = Bs_data.find("biblebook", {"bname": lambda x: x and x.lower() == bk})
            if not book:
                return f"Book '{bk}' not found.", f"Book '{bk}' not found."
            
            # Find chapter based on chapter number
            chapter = book.find("chapter", {"cnumber": chpt})
            if not chapter:
                return f"Chapter '{chpt}' not found.", f"Chapter '{chpt}' not found."
            
            # If specific verses are requested
            if vs:
                range_match = re.match(r"(\d+)-(\d+)", vs)
                verses = chapter.find_all("vers")
                if range_match:
                    start_verse = int(range_match.group(1))
                    end_verse = int(range_match.group(2))
                    for v in verses:
                        vnum = int(v["vnumber"])
                        if start_verse <= vnum <= end_verse:
                            result.append(f"{v['vnumber']}: {v.text.strip()}")
                else:
                    verse = chapter.find("vers", {"vnumber": vs})
                    if verse:
                        result.append(f"{verse['vnumber']}: {verse.text.strip()}")
                    else:
                        return f"Verse '{vs}' not found.", f"Verse '{vs}' not found."
            else:
                # If no specific verse is provided, return all verses from the chapter
                for v in chapter.find_all("vers"):
                    result.append(f"{v['vnumber']}: {v.text.strip()}")
            
            # Combine the results into a single string with spaces in between
            resultStr = " ".join(result)
            return result, resultStr

        except Exception as e:
            return f"Error: {e}", f"Error: {e}"
    else:
        return "Invalid reference format.", "Invalid reference format."

# Main function to continuously accept user input
if __name__ == "__main__":
    while True:
        # Taking user input for version and scripture reference
        vrs = input("Enter Version (e.g., ESV, NKJV, NLT, RV09): ")
        inp = input("Enter scripture reference (e.g., Genesis 1:1-2): ")  # Regex for reference input

        resultList, resultStr = search_verse(vrs, inp)

        # Print the result as a single string with spaces between verses
        print(resultStr)
        print("---------------------------------------------------/n")
