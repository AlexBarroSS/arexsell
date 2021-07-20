class AuthRepository {
  Future<void> login() async {
    print("login");
    print("login ok");

    throw Exception("Login Falhou");
  }
}
