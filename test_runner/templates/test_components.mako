<%!
	from django.core.urlresolvers import reverse
%>
<%def name="header(title='MooTools Test Framework', projects=False, current=None, previous=None, next=None)">
	<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
	<html>
		<head>
			<title>${title_prefix} - ${title}</title>
			<link rel="stylesheet" href="/static/css/reset.css" type="text/css" media="screen" title="no title" charset="utf-8">
			<link rel="stylesheet" href="/static/css/tests.css" type="text/css" media="screen" title="no title" charset="utf-8">
			
		</head>
		<body class="not_loaded">
		
			${nav(title=title, projects=projects, current=current, previous=previous, next=next)}
			<div id="mt-content">
				<div id="mt-loading">Loading scripts...</div>
</%def>

<%def name="footer()">
			</div>
			<script>
				document.body.className = 'loaded';
			</script>
		</body>
	</html>
</%def>

<%def name="nav(title, projects, current=None, previous=None, next=None)">
	<div id="mt-nav">
		<h1>${title_prefix}</h1>
		% for project, directories in projects.iteritems():
			<h2>${project}</h2>
			% for directory in directories:
				<dl class="mt-tests">
					<dt>${directory['subdir']}</dt>
					<dd>
						<ul>
							% for file_path, file_title in directory['file_dict'].iteritems():
								<%
									klass = ""
									if file_path == str(current):
										klass = "mt-selected"
								%>
								<li class="${klass}"><span></span><a href="/test${file_path}">${file_title}</a></li>
								% endfor
						</ul>
					</dd>
				</dl>
			% endfor
		% endfor
	</div>
	<div id="mt-content_header">
		<h2>${title}</h2>
		<div>
		% if previous:
			<a class="mt-prev minibutton btn-left" href="/test${previous}"><span><span class="icon"></span>previous</span></a>
		% endif
		% if next:
		<a class="mt-next minibutton btn-right" href="/test${next}"><span><span class="icon"></span>next</span></a>
		% endif
		</div>
	</div>
</%def>