import json
import os
import pytest
import logging
from datetime import datetime
from pathlib import Path

from pytest_metadata.plugin import metadata_key


# Create custom logger
def create_logger():
    logger = logging.getLogger('pytest')
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s (%(filename)s:%(lineno)s)',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create and configure file handler
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = Path("./logs")
    log_dir.mkdir(exist_ok=True)
    
    file_handler = logging.FileHandler(
        log_dir / f"test_{timestamp}.log",
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Add handler to logger
    logger.addHandler(file_handler)
    return logger

@pytest.fixture(scope="session")
def logger():
    """Provide logger fixture for test cases"""
    return create_logger()

@pytest.fixture(autouse=True)
def log_test_info(request, logger):
    """Automatically log test start and end"""
    test_name = request.node.name
    logger.info(f"Starting test: {test_name}")
    
    yield
    
    # Log test result
    if hasattr(request.node, 'rep_call'):
        result = "PASSED" if request.node.rep_call.passed else "FAILED"
        logger.info(f"Test completed: {test_name}, Result: {result}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to get test results"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# 1、修改报告标题
def pytest_html_report_title(report):
    report.title = "测试报告"


# 2、运行测试前修改环境信息
def pytest_configure(config):
    config.stash[metadata_key]["项目名称"] = "我的测试项目名称"
    config.stash[metadata_key]["接口模块"] = "我的测试接口模块"
    config.stash[metadata_key]["接口地址"] = "我的测试接口地址"

    # 3、动态生成log文件的名称，哪怕配置文件中配置了log_file选项也不会生效
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    config.option.log_file = os.path.join(config.rootdir, 'log', f'{time_now}.log')


# 4、修改摘要信息
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend(["<p>所属部门: 测试xxx部门</p>"])
    prefix.extend(["<p>测试人员: 张三xxxxxx</p>"])


# 5、修改测试结果表格中的列（插入列）
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>描述</th>")
    cells.insert(1, '<th class="sortable time" data-column-type="time">测试时间</th>')


# 6、修改测试结果表格中的列（插入数据）
def pytest_html_results_table_row(report, cells):
    cells.insert(2, f"<td>{report.description}</td>")
    cells.insert(1, f'<td class="col-time">{datetime.utcnow()}</td>')


# 7、获取测试函数中的doc注释
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)

    # 8、获取测试函数中的异常错误信息
    if call.excinfo is not None:
        msg = {
            "module": item.location[0],
            "function": item.name,
            "line": item.location[1],
            "message": str(call.excinfo.value).replace("\n", ":")
        }
        logging.error(json.dumps(msg, indent=4, ensure_ascii=False))