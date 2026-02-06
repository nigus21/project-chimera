import inspect
import skills

def test_skill_modules_exist():
    """
    Ensures that skill modules are discoverable and structured.
    """
    assert hasattr(skills, "__path__")

def test_skill_readme_presence():
    """
    Ensures every skill has a README defining its contract.
    """
    import os

    skills_dir = "skills"
    for skill_name in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_name)
        if os.path.isdir(skill_path):
            readme_path = os.path.join(skill_path, "README.md")
            assert os.path.exists(readme_path), f"{skill_name} missing README.md"