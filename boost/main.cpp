// g++ -o main main.cpp -lboost_thread

#include <boost/thread/thread.hpp>
#include <iostream>

using namespace std;

void hello_world()
{
    cout << "Здравствуй, мир, я - thread!" << endl;
}

int main(int argc, char* argv[])
{
    // запустить новый поток, вызывающий функцию "hello_world"
    boost::thread my_thread(&hello_world);
    // ждём завершения потока
    my_thread.join();

    return 0;
}
