#include <QtCore>
#include <QtConcurrent/QtConcurrent>
#include <QImage>

QString myToUpper(const QString &str) {
    qDebug() << str << "\tThread:" << QThread::currentThreadId();
    return str.toUpper();
}

QImage scale(const QImage &image) {
    qDebug() << "Scaling image in thread" << QThread::currentThread();
    return image.scaled(QSize(100, 100), Qt::IgnoreAspectRatio, Qt::SmoothTransformation);
}

int main(int argc, char* argv[]) {
    QCoreApplication app(argc, argv);
    
    // run()
    QFuture<QString> future = QtConcurrent::run(myToUpper, QString("test"));
    future.waitForFinished();
    qDebug() << future.result();
    
    // mapped()
    QStringList lst(QStringList() << "one" << "two" << "three");
    QFuture<QString> future2 = QtConcurrent::mapped(lst.begin(), lst.end(), myToUpper);
    future2.waitForFinished();
    qDebug() << future2.results();
    
    // blockingMapped()
    constexpr int imageCount = 1000;
    QList<QImage> images;
    for (int i = 0; i < imageCount; ++i) {
        images.append(QImage(1600, 1200, QImage::Format_ARGB32_Premultiplied));
    }
    QList<QImage> thumbnails = QtConcurrent::blockingMapped(images, scale);
    qDebug() << "===";
    
    return 0;
}
