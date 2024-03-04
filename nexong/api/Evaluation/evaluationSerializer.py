from rest_framework import serializers
from nexong.models import EvaluationType, StudentEvaluation, Lesson
from rest_framework.serializers import ModelSerializer


# TO-DO: Add validation if the date of the grade goes beyond the date of the lesson


class StudentEvaluationSerializer(ModelSerializer):
    evaluation_type = serializers.PrimaryKeyRelatedField(
        queryset=EvaluationType.objects.all(), required=True
    )
    url = serializers.HyperlinkedIdentityField(view_name="studentevaluation-detail")

    class Meta:
        model = StudentEvaluation
        fields = [
            "id",
            "grade",
            "date",
            "comment",
            "student",
            "evaluation_type",
            "url",
        ]

    def validate(self, attrs):
        validation_error = {}

        evaluation_type = attrs.get("evaluation_type")
        grade = attrs.get("grade")
        grade_range = evaluation_type.grade_system

        if grade_range == "ZERO_TO_ONE":
            if grade > 1:
                validation_error["grade"] = (
                    "The grade must be in range from 0 to 1 for this evaluation type."
                )

        elif grade_range == "ONE_TO_FIVE":
            if grade > 5 or grade < 1:
                validation_error["grade"] = (
                    "The grade must be in range from 1 to 5 for this evaluation type."
                )

        if validation_error:
            raise serializers.ValidationError(validation_error)

        return attrs


class EvaluationTypeSerializer(ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(), required=True
    )
    url = serializers.HyperlinkedIdentityField(view_name="evaluationtype-detail")

    class Meta:
        model = EvaluationType
        fields = [
            "id",
            "name",
            "description",
            "evaluation_type",
            "grade_system",
            "lesson",
            "url",
        ]
