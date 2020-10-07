/* Class : HastTable
 * Function : A completed Hash table class
 * Author : Jason
 * Date : 2014.03.16
 */
class Entry
{
private:
    int m_nKey;
    string m_strData;
public:
    friend bool operator==(const Entry& E1, const Entry& E2);
    Entry();
    Entry(const int& nKey, const string& strData);
    ~Entry();
    void SetKey(int nKey);
    void SetData(const string& strData);
    int GetKey() const;
    string GetData() const;
};

bool operator==(const Entry& E1, const Entry& E2)
{
    return E1.m_nKey == E2.m_nKey ? true : false;
}

Entry::Entry()
{}
Entry::Entry(const int& nKey, const string& strData)
{
    m_nKey = nKey;
    m_strData = strData;
}
Entry::~Entry()
{
    m_nKey = 0;
    m_strData = '\0';
}
void Entry::SetKey(int nKey)
{
    m_nKey = nKey;
}
void Entry::SetData(const string& strData)
{
    m_strData = strData;
}
int Entry::GetKey() const
{
    return m_nKey;
}
string Entry::GetData() const
{
    return m_strData;
}

class EntryHashTable
{
public:
    typedef list<Entry>::const_iterator ListEntryIter;
private:
    list<Entry> m_Container[10];
    int HashFunction(const int& entry) const;
    int m_Count;
public:
    EntryHashTable();
    ~EntryHashTable();
    void Insert(const Entry& entry);
    bool Find(const Entry& entry) const;
    bool Delete(const Entry& entry);
    int Count() const;
};

int EntryHashTable::HashFunction(const int& v) const
{
    return v%10;
}

EntryHashTable::EntryHashTable()
{
    
}

EntryHashTable::~EntryHashTable()
{
    for (int i = 0; i < 10; i++)
    {
        m_Container[i].clear();
    }
    m_Count = 0;
}

void EntryHashTable::Insert(const Entry& entry)
{
    int HashRes = HashFunction(entry.GetKey());
    m_Container[HashRes].push_back(entry);
    ++m_Count;
}

bool EntryHashTable::Find(const Entry& entry) const
{
    int HashRes = HashFunction(entry.GetKey());
    ListEntryIter FindIter;
    for (FindIter = m_Container[HashRes].begin(); FindIter != m_Container[HashRes].end(); ++FindIter)
    {
        if (*FindIter == entry)
        {
            return true;
        }
    }
    return false;
}

bool EntryHashTable::Delete(const Entry& entry)
{
    int HashRes = HashFunction(entry.GetKey());
    ListEntryIter DelIter;
    for (DelIter = m_Container[HashRes].begin(); DelIter != m_Container[HashRes].end(); ++DelIter)
    {
        if (*DelIter == entry)
        {
            m_Container[HashRes].erase(entry);
            --m_Count;
            return true;
        }
    }
    return false;
}

int EntryHashTable::Count() const
{
    return m_Count;
}