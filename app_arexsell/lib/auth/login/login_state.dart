import 'package:app_arexsell/auth/form_submission_status.dart';

class LoginState {
  final String user;
  bool get isValidUser => user.length >= 3;

  final String password;
  bool get isValidPassword => password.length >= 6;

  final FormSubmissionStatus formStatus;

  LoginState({
    this.user = '',
    this.password = '',
    this.formStatus = const InitialFormStatus(),
  });

  LoginState copyWith({
    String? user,
    String? password,
    FormSubmissionStatus? formStatus,
  }) {
    return LoginState(
      user: user ?? this.user,
      password: password ?? this.password,
      formStatus: formStatus ?? this.formStatus,
    );
  }
}
