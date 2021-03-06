# Create your views here.

from djangomako.shortcuts import render_to_response, render_to_string
import os, re
from django.conf import settings
from django.http import HttpResponse

def index(request):
  projects, flat_list = get_files()
  return render_to_response('index.mako', 
    {
      'flat_list': flat_list,
      'projects': projects,
      'title_prefix': settings.TITLE_PREFIX,
      'current': None,
      'next': None,
      'previous': None
    }
  )

def test(request, path):
  projects, flat_list = get_files()
  full_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ext", path))

  try:
    current_index = flat_list.index(full_path)
  except:
    raise Exception("The path %s was not found." % path)
  
  next = current_index + 1
  prev = current_index - 1
  if prev >= 0:
    prev = get_short_path(flat_list[prev])
  else:
    prev = None
  if next < len(flat_list):
    next = get_short_path(flat_list[next])
  else:
    next = None

  if full_path in flat_list:
    f = open(full_path)
    return render_to_response('test.mako', 
      {
        'test': f.read(),
        'title': make_title(path),
        'current': '/' + path,
        'projects': projects,
        'flat_list': flat_list,
        'title_prefix': settings.TITLE_PREFIX,
        'previous': prev,
        'next': next
      }
    )
    
  else:
    raise Exception("The path you requested is not a valid test path.")

HTML_MATCHER = re.compile("\.html$")

def get_short_path(full_path):
  return full_path.replace(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ext")), "")

def get_files():
  dirs = dict()
  for project, directory in settings.MOOTOOLS_TEST_LOCATIONS.iteritems():
    files = []
    project_as_title = make_title(project)
    dirs[project_as_title] = []
    for root, subdirs, files in os.walk(directory):
      for subdir in subdirs:
        testfiles = [os.path.join(directory, subdir, name) for name in os.listdir(os.path.join(directory, subdir)) if HTML_MATCHER.search(name)]
        dirs[project_as_title].append(dict(
          subdir=make_title(subdir),
          files=testfiles,
          file_dict=get_file_dict(testfiles)
        ))

  flat_list = []
  for project, directories in dirs.iteritems():
    for directory in directories:
      flat_list.extend(directory['files'])
  return dirs, flat_list

def get_file_dict(files):
  return dict([(file.split('ext')[1], make_title(file.split('ext')[1])) for file in files])

def make_title(path):
  return path.split('/')[-1].replace('.html', '').replace('_', ' ').title()