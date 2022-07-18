from flask import Blueprint, render_template, request, url_for
from zapController import crawl

bp = Blueprint('crawl', __name__, url_prefix='/crawl')


@bp.route('/', methods=['GET'])
def crawler_index():
    return render_template('crawler/main.html',
                           title='index',
                           content='Hello World')


@bp.route('/run', methods=['GET'])
def run_crawler_get():
    return render_template('crawler/form.html',
                           title='run crawler',
                           content=[
                               {'name': 'api_key', 'type': 'text', 'placeholder': 'ZAP API Key'},
                               {'name': 'url', 'type': 'text', 'placeholder': 'URL to run the spider'},
                               {'name': 'submit', 'type': 'submit', 'placeholder': ''}],
                           target=url_for('crawl.run_crawler_post'))


@bp.route('/run', methods=['POST'])
def run_crawler_post():
    api_key = request.form.get('api_key')
    url = request.form.get('url')

    res = crawl.start_crawl(url=url, api_key=api_key)

    return render_template('crawler/main.html',
                           title='crawler status',
                           content=f'<h1>crawler started <span style="color:{"blue" if res[0] else "red"}">'
                                   f'{"successfully" if res[0] else "error"}</span></h1><br /><br />'
                                   f'{"scanId" if res[0] else "errormsg"}: {res[1]}')


@bp.route('/status', methods=['GET'])
def crawler_status_get():
    return render_template('crawler/form.html',
                           title='crawler status',
                           content=[
                               {'name': 'api_key', 'type': 'text', 'placeholder': 'ZAP API Key'},
                               {'name': 'crawl_id', 'type': 'text', 'placeholder': 'Spider ID'},
                               {'name': 'submit', 'type': 'submit', 'placeholder': ''}],
                           target=url_for('crawl.crawler_status_post'))


@bp.route('/status', methods=['POST'])
def crawler_status_post():
    # TODO keep updated using AJAX
    api_key = request.form.get('api_key')
    scan_id = request.form.get('crawl_id')

    res = crawl.view_status(scan_id=scan_id, api_key=api_key)

    return render_template('crawler/main.html',
                           title='crawler status',
                           content=f'<h1>crawler status lookup <span style="color:{"blue" if res[0] else "red"}">'
                                   f'{"successfully" if res[0] else "error"}</span></h1><br /><br />'
                                   f'{"status" if res[0] else "errormsg"}: {res[1]}')


@bp.route('/find_input', methods=['GET'])
def crawler_find_input_vector_get():
    return render_template('crawler/form.html',
                           title='find input vector',
                           content=[
                               {'name': 'api_key', 'type': 'text', 'placeholder': 'ZAP API Key'},
                               {'name': 'crawl_id', 'type': 'text', 'placeholder': 'Spider ID'},
                               {'name': 'submit', 'type': 'submit', 'placeholder': ''}],
                           target=url_for('crawl.crawler_find_input_vector_post'))


@bp.route('/find_input', methods=['POST'])
def crawler_find_input_vector_post():
    # TODO non-block
    api_key = request.form.get('api_key')
    scan_id = request.form.get('crawl_id')

    res = crawl.find_vector_input(scan_id=scan_id, api_key=api_key)

    if res[0]:
        return render_template('crawler/search_result.html',
                               title='find input vector',
                               subject='find input vector from crawled pages',
                               results=res[1])
    else:
        return render_template('crawler/search_result.html',
                               title='find input vector',
                               subject='find input vector from crawled pages',
                               errormsg=res[1])
