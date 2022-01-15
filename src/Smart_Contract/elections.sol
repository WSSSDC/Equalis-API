pragma solidity >=0.7.0 <0.9.0;

contract ElectionsContract {
    //Model a candidate
    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }
    // Model election
    struct Election {
        uint256 id;
        string name;
        bool start;
        bool end;
        // Store accounts which have voted
        mapping(uint256 => bool) voters;
        mapping(uint256 => Candidate) candidates;
        // Store Candidate Count
        uint256 candidatesCount;
    }

    // Store Elections
    mapping(uint256 => Election) elections;
    // Store Election Count
    uint256 electionsCount;

    modifier validateElection(uint256 _electionID) {
        require(_electionID > 0 && _electionID <= electionsCount);
        _;
    }

    modifier validateCandidate(uint256 _electionID, uint256 _candidateID) {
        require(
            _candidateID > 0 &&
                _candidateID <= elections[_electionID].candidatesCount
        );
        _;
    }

    // // voted event
    // event votedEvent(uint256 indexed _candidateId);

    // Constructor
    // constructor() public {
    //     addCandidate("Candidate 1");
    //     addCandidate("Candidate 2");
    // }

    function createElection(string memory _name)
        public
        returns (uint256 electionID)
    {
        electionID = electionsCount++;
        elections[electionID].id = electionsCount;
        elections[electionID].name = _name;
        elections[electionID].start = false;
        elections[electionID].end = false;
    }

    function createCandidate(uint256 _electionID, string memory _name)
        public
        validateElection(_electionID)
        returns (uint256 candidateID)
    {
        // require that the election has not started
        require(!elections[_electionID].start);
        // require that the election has not finished
        require(!elections[_electionID].end);
        // create candidateID
        candidateID = elections[_electionID].candidatesCount++;
        elections[_electionID].candidates[candidateID] = Candidate(
            candidateID,
            _name,
            0
        );
    }

    function vote(
        uint256 _electionID,
        uint256 _candidateID,
        uint256 _userID
    )
        public
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
    {
        // require that the election has started
        require(elections[_electionID].start);

        // require that the election has not finished
        require(!elections[_electionID].end);

        // require that address hasn't voted before
        require(!elections[_electionID].voters[_userID]);

        // record that voter has voted
        elections[_electionID].voters[_userID] = true;

        // update candidate vote count
        elections[_electionID].candidates[_candidateID].voteCount++;

        // trigger vote event
        // emit votedEvent(_candidateId);
    }

    function startElection(uint256 _electionID)
        public
        validateElection(_electionID)
    {
        // require that the election has not started
        require(!elections[_electionID].start);
        // require that the election has not finished
        require(!elections[_electionID].end);
        elections[_electionID].start = true;
    }

    function endElection(uint256 _electionID)
        public
        validateElection(_electionID)
    {
        // require that the election has not finished
        require(!elections[_electionID].end);
        elections[_electionID].end = true;
    }

    function getElectionsCount() public returns (uint256) {
        return electionsCount;
    }

    function getVotes(uint256 _electionID, uint256 _candidateID)
        private
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
        returns (uint256 votes)
    {
        votes = elections[_electionID].candidates[_candidateID].voteCount;
    }
}
