"""
    �ļ�����,open()����һ��file����r+��ģʽΪ������Ҳ����д�� w+��ģʽΪд����Ҳ���Զ�
    1- ���"r"�ķ�ʽ�򿪣������ڻᱨ���쳣�����ڵĻ���򿪲��ҷ��ظö���
    2- ���"w"�ķ�ʽopen�������ڵ��ļ����ᱨ�����ǻ�**����**һ���µ��ļ�
    3- ��ȡ��д���ʱ����write��κ�read��Σ�ֻ��open-close֮���ٴβ�����������Ч
"""
# �ļ��Ĵ�
a_file = open("Test.txt", "w+")
# �ļ��Ķ�д
a_file.write("Hello World!")
# �ر��ļ�
a_file.close()

"""
    1- read(2) ��ȡ2���ֽڣ� �޲α�ʾ��ȡȫ��
    2- readline() ��ȡһ�У��ٴ�readline()�ͻ����ȡ��һ��
"""
b_file = open("Test.txt", "r")
result = b_file.read()
print(result)
b_file.close()

"""
    ���ĵ����⣬������open��ʱ��ؼ��ֲ���ָ������open(encoding="utf-8")
    file�ķ���ģʽ��
    1- "w" �������д�룬���ı��ķ�ʽд�뱣��
    2- "r" �����ڻ�ֱ���쳣����
    3- "a" -> append׷�ӣ�Ҳ��д���һ��
    4- "rb" ��ȡ��������,��ʾ�Ķ���16���Ƶ����֣���Ҫ����decode
    5- "wb" �Զ����Ƶķ�ʽд�룬 ���淽ʽ�Ĳ�ͬ��ֱ�ӱ����ı��ᱨ����Ҫ.encode("utf-8")����
"""
c_file = open("Test.txt","wb")
c_file.write("�й�".encode("utf-8"))  # �ı�.encodeѹ��
c_file.close()

d_file = open("Test.txt","rb")     # ����ֻ��read(3)��ʾһ������
result = d_file.read().decode(encoding="utf-8")     # �����ƶ�ȡ�Ľ���
print(result)


