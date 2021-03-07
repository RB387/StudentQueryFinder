from lib.entities import StudentGrade


class TestStudent:
    def test_from_dict(self):
        as_dict = {
            'last_name': 'name',
            'subject': 'subj',
            'semester': '1',
            'grade': '14',
        }
        student = StudentGrade.from_dict(as_dict)

        assert student == StudentGrade(
            last_name='name',
            subject='subj',
            semester='1',
            grade='14',
        )

    def test_as_dict(self):
        student_grade = StudentGrade(
            last_name='name',
            subject='subj',
            semester='1',
            grade='14',
        )

        assert student_grade.as_dict() == {
            'last_name': 'name',
            'subject': 'subj',
            'semester': '1',
            'grade': '14',
        }