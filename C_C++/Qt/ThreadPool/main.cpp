#include <QtCore>

/**
 * QThreadPool manages and recyles individual QThread objects to help reduce thread creation costs in programs that use threads.
 * Each Qt application has one global QThreadPool object, which can be accessed by calling globalInstance().
 * To use one of the QThreadPool threads, subclass QRunnable and implement the run() virtual function.
 * Then create an object of that class and pass it to QThreadPool::start().
 * QThreadPool deletes the QRunnable automatically by default.
 * Calling start() multiple times with the same QRunnable when autoDelete is enabled creates a race condition and is not recommended.
 * Threads that are unused for a certain amount of time will expire. The default expiry timeout is 30000 milliseconds (30 seconds).
 * Note that QThreadPool is a low-level class for managing threads, see the Qt Concurrent module for higher level alternatives.
 */

class HelloWorldTask : public QRunnable {
    void run() override {
        qDebug() << "Hello world from thread" << QThread::currentThread();
    }
};

int main(int argc, char* argv[]) {
    QCoreApplication app(argc, argv);
    
    auto *hello = new HelloWorldTask();
    // QThreadPool takes ownership and deletes 'hello' automatically
    QThreadPool::globalInstance()->start(hello);
    
    return 0;
}
