/*
处理userid-timestamp-artid-artname-traid-traname.tsv文件，筛选出请求内容最少的100个用户，保留他们的内容

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

const int userNum = 100;  // 用户数量
ifstream inFile;
ofstream outFile;
vector<pair<string, int>> users;  // 每个用户id请求的数量
vector<requestData> data;
map<string, bool> vis;  // 标记请求数据量前100的用户id
map<string, int> cnt;   // 存储每一个userid请求的数据数量

template <typename T>
T read(const string &inFilePath) {
    T inFile(inFilePath, ios::binary);
    if (inFile.is_open()) {
        cout << "成功打开" << inFilePath << endl;
        return inFile;
    }
    cout << "[ERROR]: 无法打开文件：" << inFilePath << " \n";
}

string getpath(string s1, string s2) {
    return s1 + "\\" + s2;
}

// user_000348	2008-01-19T11:27:58Z	66cc244d-6f96-4668-a6e9-0f9cd5acc940	Gotan Project	90f74029-93cd-4cf4-a8df-67b3c392fe4d	Chunga'S Revenge
void getMostUsers(map<string, int> &cnt) {
    cout << "正在计算每一位用户请求数据量..." << endl;
    inFile = read<ifstream>(getpath(inFilePath, fileName));
    if (!inFile.is_open()) return;
    string line;
    int js = 0;
    while (getline(inFile, line)) {
        js++;
        string userId = line.substr(0, line.find('\t'));
        cnt[userId]++;
    }
    cout << "计算完成: 一共有" << js << "条数据\n";
    inFile.close();
}

void writeFile() {
    cout << "正在写入文件" << endl;
    outFile = read<ofstream>(getpath(outFilePath, outFileName1));
    if (!outFile.is_open()) return;
    for (int i = 0; i < data.size(); i++) {
        outFile << data[i].user_id << "\t" << data[i].time << "\t" << data[i].song << "\t" << data[i].author << endl;
    }
    cout << "写入完成" << endl;
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
    cout << "正在取出前" << userNum << "个用户...." << endl;
    int js = 0;
    while (getline(inFile, line)) {
        // cout << js << ": ";
        // cout << line << endl;
        if (containChinese(line)) {
            // cout << "第" << js << "条记录包含中文，过滤掉" << endl;
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
                // 如果user_id不是前100
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
    cout << "处理完成，处理了" << js << "条记录" << endl;
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
    // 按请求内容数量从大到小排序
    sort(users.begin(), users.end(), [=](pair<string, int> a, pair<string, int> b) {
        return a.second > b.second;
    });
}

// 取出前userNum个用户，写入most100Datas.tsv
void process1() {
    // 读取文件内容计算每一个用户请求次数
    getMostUsers(cnt);

    // 从大到小排序
    sortGreater();

    // 写入前userNum名用户的信息
    writeMostUserNumToFile();

    // // 取出前userNum个用户，储存到data数组中
    // getMostUsers();

    // // 把data数组写入文件
    // writeFile();
}

void readData() {
    cout << "开始读入数据" << endl;
    data.clear();
    inFile = read<ifstream>(getpath(outFilePath, outFileName1));
    if (!inFile.is_open()) return;
    string line;
    while (getline(inFile, line)) {
        istringstream iss(line);
        string token;
        vector<string> tokens;

        // 通过\t分隔字符串，并存储到向量中
        while (getline(iss, token, '\t')) {
            tokens.push_back(token);
        }

        data.push_back(requestData(tokens[0], tokens[1], tokens[2], tokens[3]));
    }
    inFile.close();
    cout << "读入完成" << endl;
}

// 把data的数据按照时间从小到大排序，写入文件
void writeData(const string &fileName) {
    cout << "开始写入数据" << endl;
    outFile = read<ofstream>(getpath(outFilePath, fileName));
    if (!outFile.is_open()) return;
    sort(data.begin(), data.end(), [&](requestData &a, requestData &b) {
        return a.time < b.time;
    });
    for (int i = 0; i < data.size(); i++) {
        outFile << data[i].user_id << "\t" << data[i].time << "\t" << data[i].song << "\t" << data[i].author << endl;
    }
    outFile.close();
    cout << "写入完成" << endl;
}

// 读取前100名用户的请求数据，并按时间排序写入outFileName2中
void process2() {
    readData();
    writeData(outFileName2);
}

// 把所有用户按请求时间排序
void process3() {
    //////
    inFile = read<ifstream>(getpath(inFilePath, fileName));
    cout << "正在读取文件..." << endl;
    if (!inFile.is_open()) return;
    string line;
    int js = 0;
    while (getline(inFile, line)) {
        if (containChinese(line)) {
            // cout << "第" << js << "条记录包含中文，过滤掉" << endl;
            js++;
            continue;
        }
        istringstream iss(line);
        string token;
        vector<string> tokens;

        // 通过空格分隔字符串，并存储到向量中
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
    cout << "处理完成: 一共有" << js << "条数据\n";
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