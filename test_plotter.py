import pytest
import plotter

@pytest.fixture
def app(qtbot):
    test_app = plotter.MainWindow()
    qtbot.addWidget(test_app)
    return test_app


@pytest.fixture(scope='function', autouse=True)
def first_app(app, request):
    request.instance.app = app
    
    
class Test_general:

    # test that no error_dialog in normal case
    def test_no_error(self, request):
        assert request.instance.app.warning.isHidden() == True

    # test submit button text
    def test_submit_text(self, request):
        assert request.instance.app.plotButton.text() == "Plot"
        

