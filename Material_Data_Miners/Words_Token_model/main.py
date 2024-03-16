from getMaterialData import getMaterialData

if __name__ == '__main__':
    getMaterialData = getMaterialData()
    text = "After clod drawing process, the yield strength and tensile strength of CNTs/Cu composites reach to 185MPa and 311MPa, respectively."

    data = getMaterialData.getMaterialData_words_token(text)
    print(data)
    data = getMaterialData.classfily_data(data)
    data.to_excel('./data.xlsx')
    print(data)
