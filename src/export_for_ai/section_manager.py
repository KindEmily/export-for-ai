import re


class SectionManager:
    def __init__(self):
        self.sections = []

    def add_section(self, block_name: str, content: str):
        # Validate block name (only alphanumeric and underscores)
        if not re.match(r'^[A-Za-z0-9_]+$', block_name):
            raise ValueError(f"Invalid block name: '{block_name}'. Use only letters, numbers, and underscores.")
        
        # Check for duplicates
        for existing_block, _ in self.sections:
            if existing_block.lower() == block_name.lower():
                raise ValueError(f"Block '{block_name}' already exists.")
        self.sections.append((block_name, content))

   
    def remove_section(self, block_name: str):
        self.sections = [
            (bn, bc) for bn, bc in self.sections if bn.lower() != block_name.lower()
        ]

    def update_section(self, block_name: str, new_content: str):
        for idx, (bn, bc) in enumerate(self.sections):
            if bn.lower() == block_name.lower():
                self.sections[idx] = (bn, new_content)
                return
        raise ValueError(f"Block '{block_name}' not found.")
    
    def get_sections_content(self) -> str:
        """
        Generates the combined string of all sections.

        :return: A string containing all sections formatted appropriately.
        """
        content = ""
        for block_name, block_content in self.sections:
            content += f"<{block_name}>\n\n{block_content}\n\n</{block_name}>\n\n"
        return content

# Initialize a global SectionManager instance
section_manager = SectionManager()
