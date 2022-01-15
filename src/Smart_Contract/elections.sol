pragma solidity >=0.7.0 <0.9.0;

contract ElectionsContract {
    //Model a candidate
    struct Candidate {
        string name;
        string description;
        uint256 voteCount;
    }
    // Model election
    struct Election {
        string name;
        bool start;
        bool end;
        // Store accounts which have voted
        mapping(string => bool) voters;
        mapping(string => Candidate) candidates;
        // Check if I have this ID
        mapping(string => bool) candidatesIDs;
        // Store Candidate Count
        uint256 candidatesCount;
        uint256 totalVoteCount;
    }

    // Store Elections
    mapping(uint256 => Election) elections;
    // Store Election Count
    uint256 electionsCount;

    modifier validateElection(uint256 _electionID) {
        require(_electionID > 0 && _electionID <= electionsCount);
        _;
    }

    modifier validateCandidate(
        uint256 _electionID,
        string memory _candidateID
    ) {
        require(elections[_electionID].candidatesIDs[_candidateID]);
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
        elections[electionID].name = _name;
        elections[electionID].start = false;
        elections[electionID].end = false;
    }

    function createCandidate(
        uint256 _electionID,
        string memory _candidateID,
        string memory _name,
        string memory _description
    ) public validateElection(_electionID) {
        // require that the election has not started
        require(!elections[_electionID].start);
        // require that the election has not finished
        require(!elections[_electionID].end);
        // create candidateID
        elections[_electionID].candidatesCount++;
        elections[_electionID].candidates[_candidateID] = Candidate(
            _name,
            _description,
            0
        );
    }

    function vote(
        uint256 _electionID,
        string memory _candidateID,
        string calldata _userID
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
        elections[_electionID].totalVoteCount++;

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

    function getElectionsCount() public view returns (uint256) {
        return electionsCount;
    }

    function getElectionName(uint256 _electionID)
        public
        view
        validateElection(_electionID)
        returns (string memory)
    {
        return elections[_electionID].name;
    }

    function getElectionVotes(uint256 _electionID)
        public
        view
        validateElection(_electionID)
        returns (uint256)
    {
        return elections[_electionID].totalVoteCount;
    }

    function getElectionCandidatesCount(uint256 _electionID)
        public
        view
        validateElection(_electionID)
        returns (uint256)
    {
        return elections[_electionID].candidatesCount;
    }

    function getCandidateName(uint256 _electionID, string memory _candidateID)
        public
        view
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
        returns (string memory)
    {
        return elections[_electionID].candidates[_candidateID].name;
    }

    function getCandidateDescription(
        uint256 _electionID,
        string memory _candidateID
    )
        public
        view
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
        returns (string memory)
    {
        return elections[_electionID].candidates[_candidateID].description;
    }

    function getCandidateVotes(uint256 _electionID, string memory _candidateID)
        public
        view
        validateElection(_electionID)
        validateCandidate(_electionID, _candidateID)
        returns (uint256)
    {
        return elections[_electionID].candidates[_candidateID].voteCount;
    }
}
