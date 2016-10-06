import couchdb
from settings import COUCHUSER, COUCHPW, ALLOWED_EXT, MEDIA
import os
import re
couch = couchdb.Server()
couch.resource.credentials = (COUCHUSER,COUCHPW)
db = couch['academy']
from uuid import uuid4
from werkzeug.utils import secure_filename

class Admin(object):
    def __init__(self, **kwargs):
        self.doc = None
        self.key = None
        if 'session' in kwargs:
            user, self.date = kwargs['session']
            self.doc = db.get(user, None)
            self.key = self.doc['_id']
        elif 'user' in kwargs:
            rows = list(db.view('admin/all', key=kwargs.get('user')))
            if rows:
                row = rows[0]
                self.doc = db[row.id]
                self.key = self.doc['_id']

class Store(object):
    def __init__(self, **kwargs):
        self.doc = None
        self.key = None
        if 'session' in kwargs:
            user, date = kwargs['session']
            self.doc = db.get(user, None)
        elif 'key' in kwargs:
            key = kwargs['key']
            self.doc = db.get(key)
        elif 'user' in kwargs:
            rows = list(db.view('store/all', key=kwargs.get('user')))
            if rows:
                row = rows[0]
                self.doc = db[row.id]
        if self.doc:
            self.key = self.doc['_id']
        
    def create(self, **kwargs):
        self.errors = []
        name = kwargs['name']
        username = kwargs['username']
        for row in db.view('store/all'):
            if row.key == username:
                self.errors = ['Username "{}" already exists'.format(username)]
                return
        password = kwargs['password']
        maint_user = kwargs['maint_user']
        maint_pw = kwargs['maint_pw']
        self.doc = {'_id': uuid4().hex,
               'type': 'store',
               'name': name,
               'username': username,
               'password': password,
               'maint_user': maint_user,
               'maint_pw': maint_pw} 
        doc_id, rev = db.save(self.doc)
        self.doc = db[doc_id]
            
    def rated_list(self):
        students = []
        for row in db.view('student/store',key=self.key):
            student = Student(key=row.id)
            students.append({'name': student.doc['name'], 
                             'key': student.doc['_id'], 
                             'courses': student.full_progress()})
        return students

class Student(object):
    def __init__(self, *args, **kwargs):
        self.doc = None
        self.induction_done = False
        key = kwargs.get('key')
        if key:
            self.doc = db[key]
        if 'name' in kwargs:    
            rows = list(db.view('student/all', key=kwargs['name']))
            if rows:
                row = rows[0]
                self.doc = db[row.id]
        self._set_attributes()
        
    def _set_attributes(self):
        if self.doc:
            self.key = self.doc.get('_id')
            self.name = self.doc.get('name')
            self.password = self.doc.get('password')
            self.progress = self.doc.get('progress')
            self.store_id = self.doc.get('store_id')
        else:
            self.key = None
            self.name = None
            self.password = None
            self.progress = None
            self.store_id = None
        
    def update(self, *args, **kwargs):
        self.doc['name'] = kwargs.get('name')
        self.doc['password'] = kwargs.get('password')
        self._set_attributes()
        db[self.doc.id] = self.doc

    def delete(self, *args, **kwargs):
        db.delete(self.doc)
        self.doc = None
        self._set_attributes()

    def create(self, *args, **kwargs):
        self.doc = {'_id': uuid4().hex,
                    'type': 'student',
                    'name': kwargs.get('name'),
                    'password': kwargs.get('password'),
                    'progress': {},
                    'store_id': kwargs.get('store_id')
                    }
        db.save(self.doc)
        self._set_attributes()
            
    def update_score(self, *args, **kwargs):
        # Student
        #    progress: {
        #           "course": {
        #                       "module": value,
        #                       "module": value
        #                       },
        #           "course": {
        #                       "module": value,
        #                       "module": value
        #                       }
        #   }
        course = kwargs.get('course')
        module = kwargs.get('module')
        score = kwargs.get('score')

        progress = self.doc['progress']
        course_dict = progress.get(course, {})
        course_dict[module] = int(score)
        progress[course] = course_dict
        self.doc['progress'] = progress
        self.progress = self.doc['progress']
        db[self.doc.id] = self.doc

    def full_list(self, store_id):
        students = []
        for row in db.view('student/store',key=store_id):
            students.append({'name': row.value,
                             'key':  row.id} )
        return students

    def course_progress(self, course_url):
        modules = []
        course = Course(url=course_url)
        progress = self.doc['progress'].get(course_url,{})
        for key in course.doc['modules'].keys():
            completed = 0
            if key in progress:
                completed = progress.get(key, 0)
            module = {'url': key,
                      'name': course.doc['modules'][key]['name'],
                      'completed': completed}
            modules.append(module)
        return sorted(modules,key=lambda k: k['name'])

    def full_progress(self):
        # Why am I having such trouble with this?
        # Course
        #    modules: {
        #           "module": {
        #                       "questions": [],
        #                       "name": "The Name",
        #                       "desc": "The Desc...",
        #                       "pdf_url": "",
        #                       "video_url": ""},
        #              }

        # Student
        #    progress: {
        #           "course": {
        #                       "module": value,
        #                       "module": value
        #                       },
        #           "course": {
        #                       "module": value,
        #                       "module": value
        #                       }
        #   }
        progress = []
        for row in db.view('course/published'):
            course = Course(key=row.id)
            course_progress = self.doc['progress'].get(row.key)
            average = 0
            if course_progress:
                total = 0
                for key in course_progress.keys():
                    total += course_progress[key]
                average = round(total / len(course.doc['modules']))
            else:
                average = 0
            progress.append( {
                              'rank': course.rank,
                              'url': course.url,
                              'name': course.name,
                              'image_url': course.image_url,
                              'completed': average
                              })
        return sorted(progress, key=lambda k: k['rank'])

class Course(object):
    def __init__(self, **kwargs):
        self.doc = None
        if kwargs.get('key'):
            self.doc = db.get(kwargs['key'])
        elif kwargs.get('url'):
            self._get_by_key(url=kwargs['url'])
        self._set_attributes()

    def _get_by_key(self, **kwargs):
        self.doc = None
        if kwargs.get('url'):   
            rows = list(db.view('course/all', key=kwargs['url']))
            if rows:
                row = rows[0]
                self.doc = db[row.id]
        self._set_attributes()
        
    def _set_attributes(self):
        if self.doc:
            db.save(self.doc)
            self.key = self.doc.get('_id')
            self.desc = self.doc.get('desc')
            self.image_url = self.doc.get('image_url')
            self.modules = self.doc.get('modules')
            self.name = self.doc.get('name')
            self.published = self.doc.get('published')
            self.rank = self.doc.get('rank')
            self.url = self.doc.get('url')
        else:
            self.key = None
            self.desc = None
            self.image_url = None
            self.modules = None
            self.name = None
            self.published = False
            self.rank = None
            self.url = None
        self.errors = []
            
    def _allowed_filetype(self, **kwargs):
        if kwargs.get('filename'):
            filename = kwargs['filename']
            filename = filename.lower()
            return '.' in filename and \
               filename.rsplit('.', 1)[1] in ALLOWED_EXT
        else:
            return False

    def upload_media(self, **kwargs):
        if kwargs.get('file'):
            file = kwargs['file']
            if file.filename:
                if self._allowed_filetype(filename=file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(MEDIA, filename))
                    return filename
                else:
                    self.errors = ['file type for "{}" not allowed'.format(file.filename)]
        return ''

    def create(self, **kwargs):
        name = kwargs['name'] 
        desc = kwargs['desc'] 
        image = kwargs['file']
        self.errors = []
        if name:
            url = '-'.join(kwargs['name'].split()).lower()
            url = re.sub("[" + "!@%^&*()$#," + "]", "", url)
            if url == 'new-course':
                url = '-'.join([url, uuid4().hex])
            self._get_by_key(url=url)
            if self.doc:
                self.errors.append('Doc "{}" already exists.'.format(url))
        else:
            self.errors.append('A course Name is required')

        if image.filename:
            if self._allowed_filetype(filename=image.filename):
                imagename = secure_filename(image.filename)
            else:
                self.errors.append('file type for "{}" not permitted'.format(
                                                                image.filename
                                                                            ))
        else:
            self.errors.append('Logo image needed 176 x 44 px')
  
        if self.errors:
            return
        image.save(os.path.join(MEDIA, imagename))
        self.doc = {
                      '_id': uuid4().hex,
                      'type': 'course',
                      'desc': desc,
                      'image_url': imagename,
                      'published': False,
                      'url': url,
                      'rank': len(db.view('course/all').rows),
                      'name': name,
                      'modules': {}
                      }
        self._set_attributes()

    def update(self, **kwargs):
        self.errors = []
        for key in ('name','file','desc','rank','modules','published'):
            if key in kwargs:
                if key == 'name':
                    name = kwargs['name']
                    if not name:
                        self.errors.append('Course requires a name')
                elif key == 'file':
                    image = kwargs[key]
                    if image.filename:
                        if self._allowed_filetype(filename=image.filename):
                            imagename = secure_filename(image.filename)
                            image.save(os.path.join(MEDIA, imagename))
                            self.doc['image_url'] = imagename
                        else:
                            self.errors.append('file type for "{}" not '
                                                'permitted'.format(
                                                             image.filename))
                else:
                    self.doc[key] = kwargs[key]
        if not self.errors:
            self._set_attributes()

    def delete(self):
        db.delete(self.doc)
        self.doc = None
        self._set_attributes()
        # Re-rank all courses
        rows = db.view('course/rank').rows
        for rank, row in enumerate(rows):
            doc = db[row.id]
            doc['rank'] = rank
            db[doc.id] = doc
        # TODO:
        #     Remove logo file from MEDIA dir
            
    def _check_questions(self, msg, questions):
        if len(questions) > 0:
            question = questions[0]
            if question['question']:
                if question['answers']:
                    ans = question['answers'][0]
                    if len(ans) > 0:
                        return msg
                    else:
                        msg.append('A question is missing answers')
                else:
                    msg.append('Question is missing answers')
            else:
                msg.append('Question text is missing')
        else:
            msg.append('Module has no questions')
        return msg

    def _check_modules(self, msg):
        for key, mod in self.modules.items():
            for k in ('name','desc','video_url','pdf_url'):
                if not mod[k]:
                    m = 'No {} for Module {}'.format(k, key)
                    msg.append(m)
                if mod['questions']:
                    msg = self._check_questions(msg, mod['questions'])
                else:
                    m = 'No Questions for Module {}'.format(key)
                    msg.append(m)
        return msg

    def complete(self):
        err = []
        if self.doc:
            if self.name:
                if self.desc:
                    if self.modules:
                        err = self._check_modules(err)
                    else:
                        err.append('No modules for this course')
                else:
                    err.append('No Description for this course')
            else:
                err.append('No Name for this course')
        else:
            err.append('This Document is blank!')
        self.errors = err
        if err:
            self.errors.append('This course cannot be published')

    def add_module(self, **kwargs):
        name = kwargs['name']
        desc = kwargs['desc']
        video = kwargs['video']
        pdf = kwargs['pdf']
        self.errors = []
        if name:
            url = '-'.join(name.split()).lower()
            url = re.sub("[" + "!@%^&*()$#," + "]", "", url)
            if url == 'new-course':
                url = '-'.join([url, uuid4().hex])
            if url in self.modules:
                self.errors.append('{},{} already exists.'.format(self.name,url))
        else:
            self.errors.append('Module requires a name')
        for key in ('video','pdf'):
            file = kwargs[key]
            if file.filename:
                if self._allowed_filetype(filename=file.filename):
                    if key == 'video':
                        videoname = secure_filename(file.filename)
                    else:
                        pdfname = secure_filename(file.filename)
                else:
                    self.errors.append('file type for "{}" not permitted'.format(
                                                                    file.filename
                                                                                ))
            else:
                self.errors.append('{} upload required'.format(key.title()))
        if self.errors:
            return
        video.save(os.path.join(MEDIA, videoname))
        pdf.save(os.path.join(MEDIA, pdfname))
        self.doc['modules'][url] = { 
                                      'name': name,
                                      'video_url': videoname,
                                      'pdf_url': pdfname,
                                      'desc': desc,
                                      'questions': [],
                                      }
        self._set_attributes()
            
    def update_module(self, **kwargs):
        url = kwargs['url']
        video = kwargs['video']
        pdf = kwargs['pdf']
        try:
            module = self.modules[url]
        except:
            self.errors = ['Error in URL. Go back to start and try again']
            return
        for key in ('name','desc'):
            if key in kwargs:
                module[key] = kwargs[key]
        err = []
        videofile = None
        if 'video' in kwargs:
            if video.filename:
                if self._allowed_filetype(filename=video.filename):
                    videofile = secure_filename(video.filename)
                else:
                    err.append('file type for "{}" not permitted'.format(file.filename))
        pdffile = None
        if 'pdf' in kwargs:
            if pdf.filename:
                if self._allowed_filetype(filename=pdf.filename):
                    pdffile = secure_filename(pdf.filename)
                else:
                    err.append('file type for "{}" not permitted'.format(file.filename))
        if err:
            self.errors = err
            return
        if videofile:
            video.save(os.path.join(MEDIA, videofile))
            module['video_url'] = videofile
        if pdffile:
            pdf.save(os.path.join(MEDIA, pdffile))
            module['pdf_url'] = pdffile
        self.doc['modules'][url] = module
        db[self.doc.id] = self.doc
        self._set_attributes()

    def delete_module(self, **kwargs):
        url = kwargs['url']
        try:
            del self.doc['modules'][url]
        except:
            self.errors = ['"{}" not found!'.format(url)]
            self.errors = ['Has something changed in the URL?']
            return
        self._set_attributes()

    def add_question(self, **kwargs):
        module = kwargs['module']
        q_txt = kwargs['question']
        self.errors = []
        if module not in self.modules:
            self.errors.append('module "{}" not found!'.format(module))
            self.errors = ['Has something changed in the URL?']
            return
        if not q_txt:
            self.errors = ['Question text required']
            return
        self.doc['modules'][module]['questions'].append({'question': q_txt,
                                                         'answers': []})
        self._set_attributes()

    def update_question(self, **kwargs):
        module = kwargs['module']
        q_txt = kwargs['question']
        self.errors = []
        if module not in self.modules:
            self.errors.append('module "{}" not found!'.format(module))
            self.errors = ['Has something changed in the URL?']
            return
        if not q_txt:
            self.errors = ['Question text required']
            return
        q_no = kwargs['question_no']
        try:
            q_no = int(q_no) - 1
            self.doc['modules'][module]['questions'][q_no]['question'] = q_txt
        except:
            self.errors = ['Question Number in the URL is wrong']
            self.errors = ['Has something changed in the URL?']
            return
        self._set_attributes()

    def delete_question(self, **kwargs):
        module = kwargs['module']
        if module not in self.modules:
            self.errors.append('module "{}" not found!'.format(module))
            self.errors = ['Has something changed in the URL?']
            return
        q_no = kwargs['question_no']
        try:
            q_no = int(q_no) - 1
            del self.doc['modules'][module]['questions'][q_no]
        except:
            self.errors = ['Question Number in the URL is wrong']
            self.errors = ['Has something changed in the URL?']
            return
        self._set_attributes()

    def add_answer(self, **kwargs):
        module = kwargs['module']
        q_no = kwargs['question']
        ans_txt = kwargs['answer']
        if not ans_txt:
            self.errors = ['Answer text required']
            return 
        result = kwargs['result']
        ans = [ans_txt, result]
        try:
            q_no = int(q_no) - 1
            self.doc['modules'][module]['questions'][q_no]['answers'].append(ans)
        except KeyError:
            self.errors = ['Error in URL. Go back to start and try again']
            return
        except IndexError:
            self.errors = ['Error in URL. Go back to start and try again']
            self.errors.append('Index={}'.format(q_no))
            return
        db[self.doc.id] = self.doc
        self._set_attributes()

    def update_answer(self, **kwargs):
        mod_url = kwargs['module']
        q_no = kwargs['question']
        a_no = kwargs['ans_no']
        ans_txt = kwargs['answer']
        if not ans_txt:
            self.errors = ['Answer text required']
            return 
        result = kwargs['result']
        ans = [ans_txt,result]
        try:
            q_no = int(q_no) - 1
            a_no = int(a_no) - 1
            self.doc['modules'][mod_url]['questions'][q_no]['answers'][a_no] = ans
        except:
            self.errors = ['Error in URL. Go back to start and try again']
            return
        db[self.doc.id] = self.doc
        self._set_attributes()

    def delete_answer(self, **kwargs):
        mod_url = kwargs['module']
        q_no = kwargs['question_no']
        a_no = kwargs['ans_no']
        self.errors = []
        try:
            q_no = int(q_no) - 1
            a_no = int(a_no) - 1
            del self.doc['modules'][mod_url]['questions'][q_no]['answers'][a_no]
        except:
            self.errors = ['Error in URL. Go back to start and try again']
            return
        db[self.doc.id] = self.doc
        self._set_attributes()
 
    def course_list(self):
        courses = []
        for row in db.view('course/all'):
            modules = []
            for module in row.value['modules'].keys():
                modules.append(module)
            courses.append( {
                             'url': row.value['url'],
                             'image_url': row.value['image_url'],
                             'desc': row.value['desc'],
                             'published': row.value.get('published'),
                             'modules': modules
                             } )
        return courses

