import sys
import os
from .components import SourceCode, Method, Classe, Data

class ReportGenerator:

	def __init__(self):
		os.makedirs("./report", exist_ok=True)
		self.file = open("./report/log.html", 'w')
		self.content = ''
		self.number_of_test_smells = 1


	def add_header(self, total_ts, qtd_ts_in_projects, projects, ts_qtd): # step 1
		self.content += '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Test Smells Analysis Report</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
	:root {
		--primary-color: #6366f1;
		--secondary-color: #8b5cf6;
		--success-color: #10b981;
		--error-color: #ef4444;
		--dark-bg: #0f172a;
		--card-bg: #1e293b;
		--text-primary: #f1f5f9;
		--text-secondary: #94a3b8;
		--border-color: #334155;
	}
	
	* {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
	}
	
	body {
		font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
		background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
		color: var(--text-primary);
		line-height: 1.6;
		padding: 2rem;
	}
	
	.container {
		max-width: 1400px;
		margin: 0 auto;
	}
	
	.header {
		text-align: center;
		padding: 3rem 0;
		margin-bottom: 2rem;
		background: var(--card-bg);
		border-radius: 20px;
		border: 1px solid var(--border-color);
	}
	
	.header-icon {
		font-size: 4rem;
		color: var(--primary-color);
		margin-bottom: 1rem;
	}
	
	h1 {
		font-size: 2.5rem;
		background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
		margin-bottom: 1rem;
	}
	
	.summary-box {
		background: var(--card-bg);
		padding: 2rem;
		border-radius: 16px;
		margin-bottom: 2rem;
		border: 1px solid var(--border-color);
	}
	
	.summary-title {
		font-size: 1.5rem;
		color: var(--text-primary);
		margin-bottom: 1rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}
	
	.summary-stats {
		font-size: 1.2rem;
		color: var(--text-secondary);
		margin-bottom: 1.5rem;
	}
	
	.file-list {
		list-style: none;
		padding: 0;
	}
	
	.file-list li {
		background: rgba(99, 102, 241, 0.1);
		padding: 0.75rem 1rem;
		margin: 0.5rem 0;
		border-radius: 8px;
		border-left: 4px solid var(--primary-color);
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}
	
	.file-list li i {
		color: var(--primary-color);
	}
	
	.smell-badge {
		background: var(--error-color);
		color: white;
		padding: 0.25rem 0.75rem;
		border-radius: 20px;
		font-size: 0.9rem;
		font-weight: 600;
		margin-left: auto;
	}
	
	.test-file-section {
		background: var(--card-bg);
		border-radius: 16px;
		padding: 2rem;
		margin-bottom: 2rem;
		border: 1px solid var(--border-color);
	}
	
	.file-header {
		margin-bottom: 1.5rem;
		padding-bottom: 1rem;
		border-bottom: 2px solid var(--border-color);
	}
	
	.file-name {
		font-size: 1.3rem;
		color: var(--primary-color);
		margin-bottom: 0.5rem;
		display: flex;
		align-items: center;
		gap: 0.5rem;
	}
	
	.file-path {
		font-size: 0.9rem;
		color: var(--text-secondary);
		font-family: 'Courier New', monospace;
	}
	
	.no-smells {
		text-align: center;
		padding: 2rem;
		color: var(--success-color);
		font-size: 1.1rem;
	}
	
	.no-smells i {
		font-size: 3rem;
		display: block;
		margin-bottom: 1rem;
	}
	
	table {
		width: 100%;
		border-collapse: collapse;
		background: rgba(15, 23, 42, 0.5);
		border-radius: 12px;
		overflow: hidden;
	}
	
	thead {
		background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
	}
	
	th {
		padding: 1rem;
		text-align: left;
		font-weight: 600;
		color: white;
		text-transform: uppercase;
		font-size: 0.85rem;
		letter-spacing: 0.5px;
	}
	
	tbody tr {
		border-bottom: 1px solid var(--border-color);
		transition: background 0.2s;
	}
	
	tbody tr:hover {
		background: rgba(99, 102, 241, 0.1);
	}
	
	tbody tr:last-child {
		border-bottom: none;
	}
	
	td {
		padding: 1rem;
		color: var(--text-secondary);
	}
	
	td:first-child {
		color: var(--text-primary);
		font-weight: 600;
		text-align: center;
	}
	
	td:nth-child(2) {
		color: var(--error-color);
		font-weight: 600;
	}
	
	.divider {
		height: 2px;
		background: linear-gradient(90deg, transparent, var(--border-color), transparent);
		margin: 2rem 0;
	}
	
	@media (max-width: 768px) {
		body { padding: 1rem; }
		h1 { font-size: 2rem; }
		table { font-size: 0.9rem; }
		th, td { padding: 0.75rem; }
	}
</style>
</head>
<body>
<div class="container">
	<div class="header">
		<i class="fas fa-flask header-icon"></i>
		<h1>Test Smells Analysis Report</h1>
	</div>
	
	<div class="summary-box">
		<div class="summary-title">
			<i class="fas fa-chart-bar"></i>
			Analysis Summary
		</div>
		<div class="summary-stats">''' 

		if (total_ts > 1 and qtd_ts_in_projects > 1):
			self.content += "<strong>" + str(total_ts) + "</strong> test smells found in <strong>" + str(qtd_ts_in_projects) + "</strong> python test files"
		elif(total_ts < 2 and qtd_ts_in_projects < 2):
			self.content += "<strong>" + str(total_ts) + "</strong> test smell found in <strong>" + str(qtd_ts_in_projects) + "</strong> python test file"
		elif(total_ts > 1 and qtd_ts_in_projects < 2):
			self.content += "<strong>" + str(total_ts) + "</strong> test smells found in <strong>" + str(qtd_ts_in_projects) + "</strong> python test file"
		else:
			self.content += "<strong>" + str(total_ts) + "</strong> test smell found in <strong>" + str(qtd_ts_in_projects) + "</strong> python test files"

		self.content += '''</div>
		<ul class="file-list">\n'''
		for x in range(len(projects)):
			self.content += '\t\t<li><i class="fas fa-file-code"></i>' + self.get_testfile_name( projects[x] ) + '<span class="smell-badge">' + str(ts_qtd[x]) + " smells</span></li>\n"
		self.content += "\t</ul>\n\t</div>\n\t<div class='divider'></div>"

	def add_table_header(self, path, qtd_ts):  # step 2
		self.content += '<div class="test-file-section">\n\t<div class="file-header">\n\t\t<div class="file-name"><i class="fas fa-file-code"></i>' + self.get_testfile_name(path) + '</div>\n\t\t<div class="file-path"><i class="fas fa-folder"></i> ' + self.get_path(path) + '</div>\n\t</div>'

		if (qtd_ts > 0):
			self.content +='''\n\t<table>
\t\t<thead>
\t\t\t<tr>
\t\t\t\t<th style="width: 5%">#</th>
\t\t\t\t<th style="width: 25%">Test Smell Type</th>
\t\t\t\t<th style="width: 50%">Method Name</th>
\t\t\t\t<th style="width: 20%">Line Numbers</th>
\t\t\t</tr>
\t\t</thead>\n'''

		else:
			self.content += '\t<div class="no-smells"><i class="fas fa-check-circle"></i>No test smells detected in this file!</div>'
		self.number_of_test_smells = 1

	def add_table_body(self, ts, method, lines):  # step 4
		self.content += '''\t\t<tbody>
\t\t\t<tr>
\t\t\t\t<td>''' + str(self.number_of_test_smells) + '''</td>
\t\t\t\t<td>''' + ts + '''</td>
\t\t\t\t<td>''' + method + '''</td>
\t\t\t\t<td>''' + str(lines)[1:-1] + '''</td>
\t\t\t</tr>
\t\t</tbody>\n'''
		self.number_of_test_smells += 1


	def add_table_close(self, qtd_ts):  # step 5
		if (qtd_ts > 0):
			self.content += '''\n\t</table>'''
		self.content += '\n</div>\n<div class="divider"></div>'

	def add_footer(self): # step 6
		self.content += "\n</div>\n</body>\n</html>\n"


	def build(self): # final step (step 7)
		self.file.write( self.content )
		self.file.close()

	def get_testfile_name(self, path):
		# Handle both Windows and Unix path separators
		path = path.replace('\\', '/')
		for x in range(len(path)-1, -1, -1):
			if (path[x] == '/'):
				return path[x+1:]
		# If no separator found, return the whole path
		return path

	def get_path(self, path):
		# Handle both Windows and Unix path separators
		path = path.replace('\\', '/')
		for x in range(len(path)-1, -1, -1):
			if (path[x] == '/'):
				return path[0:x+1]
		# If no separator found, return empty string
		return ""