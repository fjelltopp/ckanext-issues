from ckan.plugins import toolkit
try:
    from ckan.new_tests import helpers
    from ckan.new_tests import factories
except ImportError:
    from ckan.tests import helpers
    from ckan.tests import factories

from ckanext.issues.tests import factories as issue_factories
from ckanext.issues.tests.helpers import (
    ClearOnTearDownMixin,
)

import bs4
from nose.tools import (assert_equals, assert_in, assert_is_not_none,
                        assert_is_none)


class TestIssueEdit(helpers.FunctionalTestBase,
                    ClearOnTearDownMixin):
    def setup(self):
        super(TestIssueEdit, self).setup()
        self.owner = factories.User()
        self.org = factories.Organization(user=self.owner)
        self.dataset = factories.Dataset(user=self.owner,
                                         owner_org=self.org['name'])
        self.issue = issue_factories.Issue(user=self.owner,
                                           dataset_id=self.dataset['id'])
        self.app = self._get_test_app()

    def test_edit_issue(self):
        # goto issue show page
        env = {'REMOTE_USER': self.owner['name'].encode('ascii')}
        response = self.app.get(
            url=toolkit.url_for('issues_show',
                                dataset_id=self.dataset['id'],
                                issue_number=self.issue['number']),
            extra_environ=env,
        )
        assert_equals(response.response.status_int, 200)

        # goto issue edit page
        response = self.app.get(
            url=toolkit.url_for('issues_edit',
                                dataset_id=self.dataset['id'],
                                issue_number=self.issue['number']),
            extra_environ=env)

        # fill in the form
        form = response.forms['issue-edit']
        form['title'] = 'edited title'
        form['description'] = 'edited description'
        # save the form
        response = helpers.webtest_submit(form, 'save', extra_environ=env)
        response = response.follow()
        # make sure it all worked
        assert_in('edited title', response)
        assert_in('edited description', response)

        result = helpers.call_action('issue_show',
                                     dataset_id=self.dataset['id'],
                                     issue_number=self.issue['number'])
        assert_equals(u'edited title', result['title'])
        assert_equals(u'edited description', result['description'])


class TestEditButton(helpers.FunctionalTestBase,
                     ClearOnTearDownMixin):
    def setup(self):
        super(TestEditButton, self).setup()
        # create a test issue, owned by a user/org
        self.owner = factories.User()
        self.org = factories.Organization(user=self.owner)
        self.dataset = factories.Dataset(user=self.owner,
                                         owner_org=self.org['name'])
        self.issue = issue_factories.Issue(user=self.owner,
                                           dataset_id=self.dataset['id'])

        self.app = self._get_test_app()

    def test_edit_button_appears_for_authorized_user(self):
        env = {'REMOTE_USER': self.owner['name'].encode('ascii')}

        response = self.app.get(
            url=toolkit.url_for('issues_show',
                                dataset_id=self.dataset['id'],
                                issue_number=self.issue['number']),
            extra_environ=env,
        )

        soup = bs4.BeautifulSoup(response.body)
        edit_button = soup.find('div', {'id': 'issue-edit-button'})
        assert_is_not_none(edit_button)

    def test_edit_button_does_not_appear_for_unauthorized_user(self):
        user = factories.User()
        env = {'REMOTE_USER': user['name'].encode('ascii')}

        response = self.app.get(
            url=toolkit.url_for('issues_show',
                                dataset_id=self.dataset['id'],
                                issue_number=self.issue['number']),
            extra_environ=env,
        )

        soup = bs4.BeautifulSoup(response.body)
        edit_button = soup.find('div', {'id': 'issue-edit-button'})
        assert_is_none(edit_button)
