import 'package:app_arexsell/auth/auth_repository.dart';
import 'package:app_arexsell/auth/form_submission_status.dart';
import 'package:app_arexsell/auth/login/login_event.dart';
import 'package:app_arexsell/auth/login/login_state.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class LoginBloc extends Bloc<LoginEvent, LoginState> {
  final AuthRepository authRepo;

  LoginBloc({required this.authRepo}) : super(LoginState());

  @override
  Stream<LoginState> mapEventToState(LoginEvent event) async* {
    if (event is LoginUserChanged) {
      yield state.copyWith(user: event.user);
    } else if (event is LoginPasswordChanged) {
      yield state.copyWith(password: event.password);
    } else if (event is LoginSubmitted) {
      yield state.copyWith(formStatus: FormSubmitting());
    }

    try {
      await authRepo.login();
      yield state.copyWith(formStatus: SubmissionSucess());
    } catch (e) {
      yield state.copyWith(formStatus: SubmissionFailed(e as Exception));
    }
  }
}
