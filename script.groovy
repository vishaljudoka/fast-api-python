def buildApp()
	{
	echo 'Building the fast api application with python on Windows OS'
	}
def testApp()
	{
	echo 'Testing the fast api application with python'
	}

def deployApp()
	{
	echo 'Deploying the afast api application with python to Production'
	echo ' Deploying vesrion ${params.version} '
	}


def sendEmail(status) {
    mail(
            to: "vishaljudoka@gmail.com",
            subject: "Build $BUILD_NUMBER - " + status + " (${currentBuild.fullDisplayName})",
            body: "Status of the Build :\n " + status + "\n\n Check console output at: $BUILD_URL/console" + "\n")
}

return this
