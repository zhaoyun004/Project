/*
 * What's a Hash Table? Why we need a Hash Table?
 * http://www.cnblogs.com/Jasonscor/p/3604336.html
 */

#include <iostream>
#include <list>

using namespace std;

class HashTable
{
public:
    typedef list<int>::iterator ListIter;
private:
    list<int> m_Container[10];
    int HashFunction(const int& v) const;
    int m_Count;
public:
    HashTable();
    ~HashTable();
    void Insert(const int& v);
    bool Find(const int& v);
    bool Delete(const int& v);
    int Count() const;
};

HashTable::HashTable()
{
    m_Count = 0;
}

HashTable::~HashTable()
{
    m_Count = 0;
    for (int i = 0; i < 10; i++)
    {
        m_Container[i].clear();
    }
}

// This Hash Function is very simple
int HashTable::HashFunction(const int& v) const
{
    return v%10;
}

int HashTable::Count() const
{
    return m_Count;
}

void HashTable::Insert(const int& v)
{
    int hashRes = HashFunction(v);
    m_Container[hashRes].push_back(v);
    ++m_Count;
}

bool HashTable::Find(const int& v)
{
    int hashRes = HashFunction(v);
    for (ListIter FindIter = m_Container[hashRes].begin(); FindIter != m_Container[hashRes].end(); ++FindIter)
    {
        if (*FindIter == v)
        {
            return true;
        }
    }
    return false;
}

bool HashTable::Delete(const int& v)
{
    int hashRes = HashFunction(v);
    for (ListIter DelIter = m_Container[hashRes].begin(); DelIter != m_Container[hashRes].end(); ++DelIter)
    {
        if (*DelIter == v)
        {
            m_Container[hashRes].erase(DelIter);
            m_Count--;
            return true;
        }
    }
    return false;
}


int main(int argc, char *argv[])
{
    HashTable h;
    h.Insert(10);
    h.Insert(12);
    h.Insert(2);
    h.Delete(2);
    if (h.Find(12))
        cout << "Find 12\n";
    cout << h.Count() << '\n';
    return 0;
}
