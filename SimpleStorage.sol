// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <8.9.0;

contract SimpleStorage {
    //variables
    uint256 favoriteNumber = 7;

    // int256 favoriteInt = -1;
    // bool favoriteBool = false;
    // string favoriteString = "Hello world";
    // address favoriteAdress = 0x71C7656EC7ab88b098defB751B7401B5f6d8976F;
    // bytes32 favoriteByte = "Hello";

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function pureFunction(uint256 _number) public pure {
        _number + _number;
    }

    //Tipos de objetos

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    //Arreglos
    People[] public people;

    // People public Persona = People({favoriteNumber: 7, name: "Crome"});

    mapping(string => uint256) public nameToFavoriteNumber;

    //Memory
    //Storage
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));

        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}