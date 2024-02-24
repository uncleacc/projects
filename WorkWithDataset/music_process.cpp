/*
����userid-timestamp-artid-artname-traid-traname.tsv�ļ���ɸѡ�������������ٵ�100���û����������ǵ�����

*/
#include <bits/stdc++.h>

#include <cctype>
using namespace std;

const string inFilePath = "E:\\MyProjects\\Experiment\\dataset\\lastfm-dataset-1K";
const string outFilePath = "E:\\MyProjects\\Experiment\\dataset\\lastfm-dataset-1K\\Processed";
const string fileName = "userid-timestamp-artid-artname-traid-traname.tsv";
const string outFileName1 = "most100Datas.tsv";
const string outFileName2 = "sortedDatas.tsv";
const string outFileName3 = "sortedDatas2.tsv";

struct requestData {
    string user_id;
    string time;
    string song;
    string author;
    requestData(string s1, string s2, string s3, string s4) {
        user_id = s1;
        time = s2;
        song = s3;
        author = s4;
    }
};

struct User {
    string id;
    char gender;
    int age;
    User(string id, char gender, int age) {
        this->age = age;
        this->id = id;
        this->gender = gender;
    }
};

const int userNum = 100;  // �û�����
ifstream inFile;
ofstream outFile;
vector<pair<string, int>> users;  // ÿ���û�id���������
vector<requestData> data;
map<string, bool> vis;  // �������������ǰ100���û�id
map<string, int> cnt;   // �洢ÿһ��userid�������������

template <typename T>
T read(const string &inFilePath) {
    T inFile(inFilePath, ios::binary);
    if (inFile.is_open()) {
        cout << "�ɹ���" << inFilePath << endl;
        return inFile;
    }
    cout << "[ERROR]: �޷����ļ���" << inFilePath << " \n";
}

string getpath(string s1, string s2) {
    return s1 + "\\" + s2;
}

// user_000348	2008-01-19T11:27:58Z	66cc244d-6f96-4668-a6e9-0f9cd5acc940	Gotan Project	90f74029-93cd-4cf4-a8df-67b3c392fe4d	Chunga'S Revenge
void getMostUsers(map<string, int> &cnt) {
    cout << "���ڼ���ÿһλ�û�����������..." << endl;
    inFile = read<ifstream>(getpath(inFilePath, fileName));
    if (!inFile.is_open()) return;
    string line;
    int js = 0;
    while (getline(inFile, line)) {
        js++;
        string userId = line.substr(0, line.find('\t'));
        cnt[userId]++;
    }
    cout << "�������: һ����" << js << "������\n";
    inFile.close();
}

void writeFile() {
    cout << "����д���ļ�" << endl;
    outFile = read<ofstream>(getpath(outFilePath, outFileName1));
    if (!outFile.is_open()) return;
    for (int i = 0; i < data.size(); i++) {
        outFile << data[i].user_id << "\t" << data[i].time << "\t" << data[i].song << "\t" << data[i].author << endl;
    }
    cout << "д�����" << endl;
    outFile.close();
    return;
}

bool containChinese(const string &line) {
    for (auto &c : line) {
        if (!isupper(c) && !islower(c) && !isascii(c)) {
            return true;
        }
    }
    return false;
}

void getMostUsers() {
    inFile = read<ifstream>(getpath(inFilePath, fileName));
    string line;
    cout << "����ȡ��ǰ" << userNum << "���û�...." << endl;
    int js = 0;
    while (getline(inFile, line)) {
        // cout << js << ": ";
        // cout << line << endl;
        if (containChinese(line)) {
            // cout << "��" << js << "����¼�������ģ����˵�" << endl;
            js++;
            continue;
        }

        vector<string> ve;
        string word;

        line += '\t';
        int flag = 0;
        // cout << line << endl;
        for (int i = 0; i < line.size(); i++) {
            if (line[i] == '\t') {
                // ���user_id����ǰ100
                if (!flag && !vis[word]) {
                    goto skip;
                }
                flag = 1;
                ve.push_back(word);
                // cout << word << "  ||  ";
                word = "";
            } else
                word += line[i];
        }
        // cout << endl;
        data.push_back(requestData(ve[0], ve[1], ve[3], ve[5]));

    skip:
        js++;
    }
    cout << "������ɣ�������" << js << "����¼" << endl;
    inFile.close();
}

void writeMostUserNumToFile() {
    outFile = read<ofstream>(getpath(outFilePath, "most100Users.txt"));
    if(!outFile) exit(-1);
    for (int i = 0; i < userNum; i++) {
        // cout << users[i].first << " " << users[i].second << endl;
        outFile << users[i].first << endl;
        vis[users[i].first] = true;
    }
    outFile.close();
}

void sortGreater() {
    for (auto p : cnt) {
        users.push_back(make_pair(p.first, p.second));
    }
    // ���������������Ӵ�С����
    sort(users.begin(), users.end(), [=](pair<string, int> a, pair<string, int> b) {
        return a.second > b.second;
    });
}

// ȡ��ǰuserNum���û���д��most100Datas.tsv
void process1() {
    // ��ȡ�ļ����ݼ���ÿһ���û��������
    getMostUsers(cnt);

    // �Ӵ�С����
    sortGreater();

    // д��ǰuserNum���û�����Ϣ
    writeMostUserNumToFile();

    // // ȡ��ǰuserNum���û������浽data������
    // getMostUsers();

    // // ��data����д���ļ�
    // writeFile();
}

void readData() {
    cout << "��ʼ��������" << endl;
    data.clear();
    inFile = read<ifstream>(getpath(outFilePath, outFileName1));
    if (!inFile.is_open()) return;
    string line;
    while (getline(inFile, line)) {
        istringstream iss(line);
        string token;
        vector<string> tokens;

        // ͨ��\t�ָ��ַ��������洢��������
        while (getline(iss, token, '\t')) {
            tokens.push_back(token);
        }

        data.push_back(requestData(tokens[0], tokens[1], tokens[2], tokens[3]));
    }
    inFile.close();
    cout << "�������" << endl;
}

// ��data�����ݰ���ʱ���С��������д���ļ�
void writeData(const string &fileName) {
    cout << "��ʼд������" << endl;
    outFile = read<ofstream>(getpath(outFilePath, fileName));
    if (!outFile.is_open()) return;
    sort(data.begin(), data.end(), [&](requestData &a, requestData &b) {
        return a.time < b.time;
    });
    for (int i = 0; i < data.size(); i++) {
        outFile << data[i].user_id << "\t" << data[i].time << "\t" << data[i].song << "\t" << data[i].author << endl;
    }
    outFile.close();
    cout << "д�����" << endl;
}

// ��ȡǰ100���û����������ݣ�����ʱ������д��outFileName2��
void process2() {
    readData();
    writeData(outFileName2);
}

// �������û�������ʱ������
void process3() {
    //////
    inFile = read<ifstream>(getpath(inFilePath, fileName));
    cout << "���ڶ�ȡ�ļ�..." << endl;
    if (!inFile.is_open()) return;
    string line;
    int js = 0;
    while (getline(inFile, line)) {
        if (containChinese(line)) {
            // cout << "��" << js << "����¼�������ģ����˵�" << endl;
            js++;
            continue;
        }
        istringstream iss(line);
        string token;
        vector<string> tokens;

        // ͨ���ո�ָ��ַ��������洢��������
        while (getline(iss, token, '\t')) {
            tokens.push_back(token);
        }
        string userId, time, song, author;
        if (tokens.size()) userId = tokens[0];
        if (tokens.size() > 1) time = tokens[1];
        if (tokens.size() > 3) song = tokens[3];
        if (tokens.size() > 5) song = tokens[3];
        data.push_back(requestData(userId, time, song, author));
        js++;
    }
    cout << "�������: һ����" << js << "������\n";
    inFile.close();
    /////////

    writeData(outFileName3);
}

int main() {
    process1();

    // process2();

    // process3();
    system("pause");
    return 0;
}