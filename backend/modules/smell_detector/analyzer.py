"""Test Smell Analyzer - Coordinates test smell detection."""

import os
from typing import List, Tuple
from .python_parser import PythonParser
from .report_generator import ReportGenerator
from typing import Dict


def is_hidden_directory(dirName: str) -> bool:
    """Check if directory is hidden."""
    return '/.' in dirName


def is_test_file(filepath: str) -> bool:
    """Check if a file is a test file based on content."""
    try:
        with open(filepath, 'r', encoding="utf8", errors='ignore') as f:
            for line in f:
                if line.find('assert') == 0:
                    return True
                if any(keyword in line for keyword in ['import unittest', 'import pytest', 'from unittest', 'from pytest']):
                    return True
    except:
        pass
    return False


def search_test_files(directory: str) -> List[str]:
    """Search for test files in a directory."""
    test_files = []
    for dirName, subdirList, fileList in os.walk(directory):
        if not is_hidden_directory(dirName):
            for filename in fileList:
                if filename.endswith('.py') and filename != 'main.py':
                    filepath = os.path.join(dirName, filename)
                    if is_test_file(filepath):
                        test_files.append(filepath)
    return test_files


class TestSmellAnalyzer:
    """Analyzes test files for test smells and generates reports."""
    
    def __init__(self):
        """Initialize the analyzer."""
        pass
    
    def analyze_file(self, filepath: str) -> dict:
        """Analyze a single test file.
        
        Args:
            filepath: Path to the test file
            
        Returns:
            Dictionary with analysis results
        """
        p = PythonParser(filepath)
        if p.ast_parser:
            logs = p.start()
        else:
            logs = p.start2()
        
        # Count unique test smells
        prev, cont = None, 0
        for log in logs:
            if log.lines != prev:
                cont += 1
            prev = log.lines
        
        return {
            'filepath': filepath,
            'logs': logs,
            'smell_count': cont
        }
    
    def analyze_files(self, file_paths: List[str]) -> Tuple[List, List[str], List[int], int]:
        """Analyze multiple test files.
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Tuple of (all_logs, projects, ts_qtd, cont_total)
        """
        all_logs, projects, ts_qtd, cont_total = [], [], [], 0
        
        for filepath in file_paths:
            result = self.analyze_file(filepath)
            all_logs.append(result['logs'])
            projects.append(filepath)
            ts_qtd.append(result['smell_count'])
            cont_total += result['smell_count']
        
        return all_logs, projects, ts_qtd, cont_total
    
    def analyze_code_string(self, code: str, filename: str = "test_code.py") -> dict:
        """Analyze test code from a string.
        
        Args:
            code: Python test code as string
            filename: Virtual filename for the code
            
        Returns:
            Dictionary with analysis results
        """
        import tempfile
        
        # Write code to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = self.analyze_file(temp_path)
            result['filepath'] = filename  # Use virtual filename in results
            return result
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except:
                pass
    
    def generate_report(self, all_logs: List, projects: List[str], ts_qtd: List[int], cont_total: int, explanations: Dict = None, output_filename: str = None) -> str:
        """Generate HTML report from analysis results.
        
        Args:
            all_logs: List of log entries from all projects
            projects: List of project paths
            ts_qtd: List of test smell quantities per project
            cont_total: Total count of test smells
            
        Returns:
            Path to generated report file
        """
        # Decide output name: AI report when explanations present
        out_name = output_filename or ("log_ai.html" if explanations else "log.html")
        report = ReportGenerator(output_filename=out_name)
        # If explanations are provided, enable explanation column early
        if explanations:
            report.include_explanation = True
        report.add_header(cont_total, len(all_logs), projects, ts_qtd)
        
        for index in range(len(all_logs)):
            prev = None  # reset per file to avoid cross-file suppression
            report.add_table_header(projects[index], ts_qtd[index])
            for log in all_logs[index]:
                if log.lines != prev:
                    if explanations:
                        key = (projects[index], getattr(log, 'method_name', ''), tuple(getattr(log, 'lines', [])))
                        explanation = explanations.get(key)
                        if explanation is not None:
                            report.add_table_body_with_explanation(log.test_smell_type, log.method_name, log.lines, explanation)
                        else:
                            report.add_table_body(log.test_smell_type, log.method_name, log.lines)
                    else:
                        report.add_table_body(log.test_smell_type, log.method_name, log.lines)
                prev = log.lines
            report.add_table_close(ts_qtd[index])
        
        report.add_footer()
        report.build()
        
        return os.path.abspath(f'./report/{out_name}')
