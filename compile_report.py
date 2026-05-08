import subprocess
import os
import sys

def compile_latex(tex_file):
    if not os.path.exists(tex_file):
        print(f"Error: {tex_file} not found.")
        return False

    print(f"Compiling {tex_file}...")
    
    # Run pdflatex twice to handle references/toc
    for i in range(2):
        try:
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                print(f"Error during compilation (Run {i+1}):")
                print(result.stdout)
                return False
        except FileNotFoundError:
            print("Error: 'pdflatex' not found. Please ensure a LaTeX distribution is installed and in your PATH.")
            return False

    pdf_file = tex_file.replace('.tex', '.pdf')
    if os.path.exists(pdf_file):
        print(f"Successfully generated {pdf_file}")
        return True
    else:
        print("Error: PDF was not generated.")
        return False

if __name__ == "__main__":
    tex_path = "Report.tex"
    success = compile_latex(tex_path)
    if not success:
        sys.exit(1)
