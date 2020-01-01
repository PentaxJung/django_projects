from django.shortcuts import render
from django.http import HttpResponse
from .models import Entries, Categories, TagModel, Comments
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import hashlib

def index(request, page=1):
	page_title = '블로그 글 목록 화면'
	
	# 글 목록 불러오기
	per_page = 5
	start_pos = (page - 1) * per_page
	end_pos = start_pos + per_page
	
	# 글 목록(페이지) 계산
	entry_count = Entries.objects.count() 
	if entry_count % per_page == 0:
		page_list = [i+1 for i in range(int(entry_count / per_page))]
	else:
		page_list = [i+1 for i in range(int(entry_count / per_page) + 1)]
	
	# 글 목록 불러오기
	entries = Entries.objects.all().select_related().order_by('-created')[start_pos:end_pos]

	tpl = loader.get_template('list.html')
	ctx = {'page_title': page_title,
		   'entries': entries,
		   'current_page': page,
		   'page_list': page_list}

	#return HttpResponse('안녕, 여러분. [%s] 글은 첫 번째 글이야.' % entries[0].Title)
	return HttpResponse(tpl.render(ctx))


def read(request, entry_id=None):
	page_title = '블로그 글 읽기 화면'

	# 글 불러오기
	try:
		current_entry = Entries.objects.get(id=int(entry_id))
	except:
		return HttpResponse('글이 존재하지 않습니다. -read ')
	
	# 이전글/다음글 처리
	try:
		prev_entry = current_entry.get_previous_by_created()
	except:
		prev_entry = None
	try:
		next_entry = current_entry.get_next_by_created()
	except:
		next_entry = None

	# 글 읽기 화면에서 댓글 불러오기
	comments = Comments.objects.filter(Entry=current_entry).order_by('created')

	tpl = loader.get_template('read.html')
	ctx = {'page_title': page_title,
		   'current_entry': current_entry,
		   'prev_entry': prev_entry,
		   'next_entry': next_entry,
		   'comments': comments,
		   }

	#return HttpResponse('안녕, 여러분. [%d]번 글은 [%s]이야.' % (current_entry.id, current_entry.Title))
	return HttpResponse(tpl.render(ctx))


def write_form(request):
	page_title = '블로그 글 쓰기 화면'

	# 카테고리 불러오기
	categories = Categories.objects.all()

	tpl = loader.get_template('write.html')
	ctx = {'page_title': page_title,
		   'categories': categories}

	return HttpResponse(tpl.render(ctx))


@csrf_exempt
def add_post(request):

	# 글 제목 처리
	# QueryDict 자료형에서는 .has_key() 사용 불가 -> in으로 대체
	if 'title' not in request.POST:
		return HttpResponse('글 제목을 입력해주세요.')
	elif len(request.POST['title']) == 0:
		return HttpResponse('글 제목에 적어도 한 글자를 입력해주세요.')
	else:
		entry_title = request.POST['title']

	# 글 내용 처리
	if 'content' not in request.POST:
		return HttpResponse('글 본문을 입력해주세요.')
	else:
		if len(request.POST['content']) == 0:
			return HttpResponse('글 본문에 적어도 한 글자는 입력해주세요.')
		else:
			entry_content = request.POST['content']

	# 글 카테고리 처리
	if 'category' not in request.POST:
		return HttpResponse('카테고리를 선택해주세요.')
	try:
		entry_category = Categories.objects.get(id=request.POST['category'])
	except:
		return HttpResponse('카테고리에 해당하는 글이 없습니다.')

	# 글 태그 처리
	if 'tags' in request.POST:
		tags = []
		split_tags = request.POST['tags'].split(',')
		for tag in split_tags:
			tags.append(tag.strip())
		tag_list = [TagModel.objects.get_or_create(Title=tag)[0] for tag in tags]
	else:
		tag_list = []

	# 새로운 글 생성 - 1차 저장
	new_entry = Entries(Title=entry_title, Content=entry_content, Category=entry_category)
	try:
		new_entry.save()
	except:
		return HttpResponse('글을 저장하는 중 오류가 발생하였습니다 - 글')
	
	# 새로운 글에 태그 붙이기
	for tag in tag_list:
		new_entry.Tags.add(tag)

	# 새로운 글 생성 - 2차 저장
	if len(tag_list) > 0:
		try:
			new_entry.save()
		except:
			return HttpResponse('글을 저장하는 중 오류가 발생하였습니다 - 태그')
	return HttpResponse('%s번 글을 성공적으로 저장하였습니다.' % new_entry.id)


@csrf_exempt
def add_comment(request):

	# 글쓴이 이름 처리
	if 'name' not in request.POST:
		return HttpResponse('글쓴이 이름을 입력해주세요.')
	else:
		if len(request.POST['name']) == 0:
			return HttpResponse('글쓴이 이름을 입력해주세요.')
		else:
			cmt_name = request.POST['name']

	# 비밀번호
	if 'password' not in request.POST:
		return HttpResponse('비밀번호를 입력해주세요.')
	else:
		if len(request.POST['password']) == 0:
			return HttpResponse('비밀번호를 입력해주세요.')
		else:
			# .encode('utf-8')을 통해 python 3.x 기본 문자열인 unicode를
			# byte 형식으로 인코딩하고 이후 md5로 hashing
			cmt_password = hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest()

	# 댓글 본문 처리
	if 'content' not in request.POST:
		return HttpResponse('댓글 내용을 입력해주세요.')
	else:
		if len(request.POST['content']) == 0:
			return HttpResponse('댓글 내용을 입력해주세요.')
		else:
			cmt_content = request.POST['content']

	# 댓글 달 글 확인
	if 'entry_id' not in request.POST:
		return HttpResponse('댓글을 달 글을 지정해주세요.')
	else:
		try:
			entry = Entries.objects.get(id=request.POST['entry_id'])
		except:
			return HttpResponse('글이 존재하지 않습니다. - add_comment')

	# 새로운 댓글 생성 - 저장
	try:
		new_cmt = Comments(Name=cmt_name, Password=cmt_password, Content=cmt_content, Entry=entry)
		new_cmt.save()

		# 글 내에서 댓글 개수 증가
		entry.Comments += 1
		entry.save()
		
		return HttpResponse('댓글을 작성하였습니다.')
	except:
		return HttpResponse('댓글을 작성하지 못했습니다.')
	return HttpResponse('댓글 작성 중에 문제가 생겼습니다.')

@csrf_exempt
def del_comment(request):
	entry = Entries.objects.get(id=request.POST['entry_id'])
	del_cmt = Comments.objects.get(id=request.POST['comment_id'], Password=hashlib.md5(request.POST['password'].encode('utf-8')).hexdigest())
	del_cmt.delete()
	entry.Comments -= 1
	entry.save()
	return HttpResponse('댓글을 삭제하였습니다.')




