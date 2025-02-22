import pytest

from openapi_spec_validator.validation.exceptions import OpenAPIValidationError


class TestLocalOpenAPIv30Validator:

    LOCAL_SOURCE_DIRECTORY = "data/v3.0/"

    def local_test_suite_file_path(self, test_file):
        return f"{self.LOCAL_SOURCE_DIRECTORY}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "petstore.yaml",
            "petstore-separate/spec/openapi.yaml",
            "parent-reference/openapi.yaml",
        ],
    )
    def test_valid(self, factory, validator_v30, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)

        return validator_v30.validate(spec, spec_url=spec_url)

    @pytest.mark.parametrize(
        "spec_file",
        [
            "empty.yaml",
        ],
    )
    def test_falied(self, factory, validator_v30, spec_file):
        spec_path = self.local_test_suite_file_path(spec_file)
        spec = factory.spec_from_file(spec_path)
        spec_url = factory.spec_file_url(spec_path)

        with pytest.raises(OpenAPIValidationError):
            validator_v30.validate(spec, spec_url=spec_url)


@pytest.mark.network
class TestRemoteOpenAPIv30Validator:

    REMOTE_SOURCE_URL = (
        "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/"
    )

    def remote_test_suite_file_path(self, test_file):
        return f"{self.REMOTE_SOURCE_URL}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/"
            "petstore.yaml",
            "f75f8486a1aae1a7ceef92fbc63692cb2556c0cd/examples/v3.0/"
            "api-with-examples.yaml",
            "970566d5ca236a5ce1a02fb7d617fdbd07df88db/examples/v3.0/"
            "api-with-examples.yaml",
        ],
    )
    def test_valid(self, factory, validator_v30, spec_file):
        spec_url = self.remote_test_suite_file_path(spec_file)
        spec = factory.spec_from_url(spec_url)

        return validator_v30.validate(spec, spec_url=spec_url)


@pytest.mark.network
class TestRemoteOpeAPIv31Validator:

    REMOTE_SOURCE_URL = (
        "https://raw.githubusercontent.com/"
        "OAI/OpenAPI-Specification/"
        "d9ac75b00c8bf405c2c90cfa9f20370564371dec/"
    )

    def remote_test_suite_file_path(self, test_file):
        return f"{self.REMOTE_SOURCE_URL}{test_file}"

    @pytest.mark.parametrize(
        "spec_file",
        [
            "comp_pathitems.yaml",
            "info_summary.yaml",
            "license_identifier.yaml",
            "mega.yaml",
            "minimal_comp.yaml",
            "minimal_hooks.yaml",
            "minimal_paths.yaml",
            "path_no_response.yaml",
            "path_var_empty_pathitem.yaml",
            "schema.yaml",
            "servers.yaml",
            "valid_schema_types.yaml",
        ],
    )
    def test_valid(self, factory, validator_v31, spec_file):
        spec_url = self.remote_test_suite_file_path(
            f"tests/v3.1/pass/{spec_file}"
        )
        spec = factory.spec_from_url(spec_url)

        return validator_v31.validate(spec, spec_url=spec_url)

    @pytest.mark.parametrize(
        "spec_file",
        [
            "invalid_schema_types.yaml",
            "no_containers.yaml",
            "server_enum_empty.yaml",
            "servers.yaml",
            "unknown_container.yaml",
        ],
    )
    def test_failed(self, factory, validator_v31, spec_file):
        spec_url = self.remote_test_suite_file_path(
            f"tests/v3.1/fail/{spec_file}"
        )
        spec = factory.spec_from_url(spec_url)

        with pytest.raises(OpenAPIValidationError):
            validator_v31.validate(spec, spec_url=spec_url)
